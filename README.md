# Sudoku solver
Created for a university assignment. Takes in a 9x9 numpy array and uses backtracking search with constraints to produce a solved sudoku. Returns the solved 9x9 array if the grid is valid and if not, returns a 9x9 array of -1.

## How to
- Function sudoku_solver takes in 9x9 numpy array of the incomplete sudoku e.g.

[[0 0 2 0 0 0 0 0 4] 

 [0 5 0 0 1 3 7 0 0] 
 
 [7 9 0 0 0 0 0 5 0] 
 
 [0 0 9 0 0 0 0 6 0] 
 
 [0 0 0 0 3 0 5 0 8] 
 
 [5 0 7 0 0 0 4 0 0] 
 
 [0 0 0 0 6 0 8 0 0] 
 
 [0 6 0 0 2 7 0 4 0] 
 
 [8 0 0 0 0 0 0 2 0]]
 
 - sudoku_solver functions returns the resultant sudoku
