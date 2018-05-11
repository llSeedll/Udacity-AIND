"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
from random import randint
import math

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def hash(game):
    aloc = str(game.get_player_location(game.active_player))
    iloc = str(game.get_player_location(game.inactive_player))
    state = str([bool(x) for x in game._board_state])
    return aloc + iloc + state


def weighted_score(game, player, my_weight=1, opp_weight=1.5):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_weight * my_moves - opp_weight * opp_moves)

def euclidean(A, B):
    d = 0
    for a, b in zip(A, B):
        d += (a - b) * (a - b)
    return d

def linearSeparation(game, player):
    separated = False
    if (not hasDiagonal(game, player)):
        for i in range(game.width):
            separated = isDiagonal(i, 0, 0, game, player, 0, 'X')
        if not separated:
            for i in range(game.height):
                separated = isDiagonal(i, 0, 0, game, player, 0, 'Y')
    else:
        separated = True
    if separated:
        my_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return (float("-inf"), float("inf"))[my_moves>opp_moves]
    return 0


def isDiagonal(x, y, direction, game, player, nbr=0, function='X'):       
    if ((x < 0 or y < 0 or x >= game.width or y >= game.height) and nbr>1):
        return True
    idx = x + y * game.height
    if len(game._board_state)<=idx:
        return False
    player_location = game._board_state[(-1, -2)[player!=game.active_player]]
    if ( game._board_state[idx] and idx == player_location):
        if function=='X':
            return isDiagonal(x + direction, y  + 1, direction, game, player, nbr+1, function) 
        elif function=='Y':
            return isDiagonal(x + 1, y  + direction, direction, game, player, nbr+1, function) 
    return False

def hasDiagonal(game, player, nbr=0):
    for i in range(game.width):
        hasDiag = isDiagonal(i, 0, 1, game, player, nbr, 'X') or isDiagonal(i, game.height - 1, 1, game, player, nbr, 'X')
        if hasDiag:
            return hasDiag
        hasDiag = isDiagonal(i, 0, -1, game, player, nbr, 'X') or isDiagonal(i, game.height - 1, -1, game, player, nbr, 'X')
        if hasDiag:
            return hasDiag

    for i in range(game.height):
        hasDiag = isDiagonal(i, 0, -1, game, player, nbr, 'Y') or isDiagonal(i, game.height - 1, -1, game, player, nbr, 'Y')
        if hasDiag:
            return hasDiag
        hasDiag = isDiagonal(i, 0, 1, game, player, nbr, 'Y') or isDiagonal(i, game.height - 1, 1, game, player, nbr, 'Y')
        if hasDiag:
            return hasDiag
    return False

def centrality(game, move):
    x, y = move
    cx, cy = (math.ceil(game.width / 2), math.ceil(game.height / 2))
    return (game.width - cx) ** 2 + (game.height - cy) ** 2 - (x - cx) ** 2 - (y - cy) ** 2

def common_moves(game, player):
    moves = game.get_legal_moves()
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    c_moves = list(set(moves).intersection(opp_moves))
    return 8 - len(c_moves)

def interfering_moves(game, player):
    cmoves = game.get_legal_moves() and game.get_legal_moves(game.get_opponent(player))
    if not cmoves:
        return 0
    return max(centrality(game, m) for m in cmoves)


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)
    
    opp = game.get_opponent(player)
    
    return float((1+len(game.get_legal_moves(player)))/(1+1.5*len(game.get_legal_moves(opp))))
       
    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parajmeters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player) 
    
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)
    p_moves = game.get_legal_moves()
    
    return float(len(p_moves) - len(opp_moves) + 2*sum(centrality(game, m) for m in p_moves) + common_moves(game, player) + interfering_moves(game, player)) 


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player) 
    
    separated = linearSeparation(game, player)
    if separated!=0:
        return separated
    
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)
    p_moves = game.get_legal_moves()
    common_moves = opp_moves and p_moves
    
    factor = 1 / (game.move_count + 1)
    ifactor = 1 / factor
    
    return float(-(1+len(common_moves) * (2*factor) )+ (ifactor)* len(game.get_legal_moves()) + weighted_score(game, player))



class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        best_move, _ = self.process(game, depth)
        return best_move

    def active_player(self, game):
        return game.active_player == self

    def process(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        if depth == 0:
            return game.get_player_location(self), self.score(game, self)
        
        if not game.get_legal_moves():
            return (-1, -1), self.score(game, self)
        
        func, value, best_move = None, None, (-1, -1)
        if self.active_player(game):
            func, value = max, float("-inf")
        else:
            func, value = min, float("inf")

        
        for move in game.get_legal_moves():
            score = self.process(game.forecast_move(move), depth-1)[1]
            if func(value, score)==score:
                value = score
                best_move = move

        return best_move, value


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """ 
    """
    We use two transposition tables to respectively store the computed best move
    for a player/position and not have to recompute it again, and store 
    the last best move of iterative deepening to start from there on the next
    iteration
    """
    tt, tt_cheat = {}, {}
        
    def get_move_order(self, game,game_hash,tt):
        moves = game.get_legal_moves()
        if game_hash in tt:
            val = tt[game_hash]
            if val in moves:
                moves.pop(moves.index(val))
                moves.insert(0,val)
        return moves

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left        
        move, depth = (-1, -1), self.search_depth
        legal_moves=game.get_legal_moves()
        if not legal_moves:
            return move
        move=legal_moves[0]
        
        self.tt = {}
        self.tt_cheat={}
        _hash = hash(game)
        while True:
            try:
                tmp_move = self.alphabeta(game, depth, _hash)
                """
                tt is a transposition table used to store the state of each game board
                after running an alphabeta search. Allowing us to avoid computing the
                same nodes multiple times during a tree search
                """
                if tmp_move!=(-1, -1):
                    move = tmp_move
                    self.tt[_hash]=move
                depth += 1
            except SearchTimeout:
                break
        return move

    def active_player(self, game):
        return game.active_player == self
    
    def alphabeta(self, game, depth, _hash=None, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        best_move, _ = self.process(game, depth, depth, _hash)
        return best_move   

    def process(self, game, depth, original_depth, _hash=None, alpha=float("-inf"), beta=float("inf"), maximize=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if depth == 0:
            return game.get_player_location(game.active_player), self.score(game, self)
        
        if not game.get_legal_moves():
            return (-1, -1), self.score(game, self)
        
        curr = game.get_player_location(game.active_player)
        value, best_move = float("-inf"), (-1, -1)
        
        """
        tt_cheat is a transposition table used to store the state of the game and
        the best move at that state for a given depth search. When exploring the game tree
        for a deeper depth, we restore the game state from the last saved depth and 
        search from there. Allowing us to search a game tree much deeper during the 
        same time limit
        """
        if depth==original_depth:
            if ((depth-1) in self.tt_cheat) and (curr in self.tt_cheat[depth-1])>0:
                b, g = self.tt_cheat[depth-1][curr]
                if len(g.get_legal_moves())>0:
                    best_move = b
                    game = g
                    
        legal_moves = self.get_move_order(game,_hash,self.tt)  
        if maximize:
            value = float("-inf")
            for move in legal_moves:
                score = self.process(game.forecast_move(move), depth-1, original_depth, _hash, alpha, beta, False)[1]
                if value<score:
                    value = score
                    best_move = move
                alpha = max(value, alpha)
                if beta <= alpha:
                    break
        else:
            value = float("inf")
            for move in legal_moves:
                score = self.process(game.forecast_move(move), depth-1, original_depth, _hash, alpha, beta, True)[1]
                if value>score:
                    value = score
                    best_move = move
                beta = min(value, beta)
                if beta <= alpha:
                    break
        
        if depth==1:
            if original_depth not in self.tt_cheat:
                self.tt_cheat[original_depth] = {}
            self.tt_cheat[original_depth][curr] = (best_move, game)

        return best_move, value

