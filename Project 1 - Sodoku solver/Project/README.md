# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve the naked twin problem using constraint propagation, it is established that if two boxes (B1, B2) who are part of a same peer have the same two possible values x and y (x=y), then the other peers of the unit they share cannot use those values. That's because the boxes are limited to two equal values so in the final solution, each will have one of the two possible values assigned to it.
To solve that problem, we eliminate the matched value from all other peers when two and only two boxes contain the same value in a unit so that no other box in that unit can have either of twin values. We could extend the solution to naked triplets or naked quadruplets...
In a sodoku game where every box will is allowed to have one of 9 choices, there are 9x9=81 boxes giving us a search space of 9^81 combinations. 
Trying every value in every box would be consuming too much time and resources on a computer. 
This technique (and in general constraint propogation techniques) allows us to considerably reduce the search space which allows us to possibly find a solution in much less time.



# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku consists of adding two other units(constraints) to the problem where the values 1-9 cannot be repeated in the diagonals of the grid.
To solve that problem, we add to the unitlist and peers additional boxes corresponding to the diagonals and then use eliminate, only choice and/or naked twins (or other constraint propagation techniques) to reduce the problem space and then apply a search algorithm.
As mentioned above constraint propogation techniques allow us to reduce the search space considerably but depending on the problem, we might have to apply a brute force search algorithm to find a solution.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

