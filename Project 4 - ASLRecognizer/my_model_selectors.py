import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    """
    base class for model selection (strategy design pattern)
    """

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        lp = {}

        for num_components in range(self.min_n_components, self.max_n_components+1, 1):
            n = num_components
            f = len(self.X[0])
            p = np.power(n,2) + 2*f*n -1


            try:
                lp[num_components] = -2 * self.base_model(num_components).score(self.X, self.lengths) + p * np.log(len(self.X))
            except:
                continue

        if  lp:
            return self.base_model(min(lp, key=lp.get))
        
        return  None


class SelectorDIC(ModelSelector):
    """ select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    """

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        dic_scores = {}
        try:
            for num_components in range(self.min_n_components,self.max_n_components+1,1):
                word_logL, rest_sum_logL = 0, 0
                model = self.base_model(num_components)
                for m in self.hwords:
                    x, l = self.hwords[m]
                    if m == self.this_word:
                        word_logL = model.score(x, l)
                    else:
                        rest_sum_logL += model.score(x, l)
                dic_scores[num_components] = word_logL - rest_sum_logL / (len(self.hwords) - 1)
        except Exception as e:
            pass
        if  dic_scores:
            return self.base_model(max(dic_scores, key=dic_scores.get))
        return  None

class SelectorCV(ModelSelector):
    """ select best model based on average log Likelihood of cross-validation folds

    """

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_score = -float("inf")
        best_num_components = self.min_n_components        
        
        if len(self.sequences) >= 3:
            num_folds = 3
            k_folds = KFold(n_splits=num_folds)
        
        for num_components in range(self.min_n_components, self.max_n_components + 1):
            score = 0
            
            if len(self.sequences) <= 2:
                try:
                    hmm_model = self.base_model(num_components)
                    score = hmm_model.score(self.X, self.lengths)
                    
                    if score > best_score:
                        best_score, best_num_components = score, num_components
                except:
                    pass
                
                continue
            
            for training_idx, test_idx in k_folds.split(self.sequences):                
                try:   
                    X_training, lengths_training = combine_sequences(training_idx, self.sequences)
                    X_test, lengths_test = combine_sequences(test_idx, self.sequences)
                   
                    hmm_model = GaussianHMM(n_components=num_components, covariance_type="diag", n_iter=1000, random_state=self.random_state, verbose=False).fit(X_training, lengths_training)
                    
                    score += hmm_model.score(X_test, lengths_test)
                except:
                    pass
                
            score /= num_folds
            
            if score > best_score:
                best_score, best_num_components = score, num_components
        
        return self.base_model(best_num_components)
