import numpy as np
import copy

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    
    def generate_initial_dict(sud):
        """Generate initial candidates for each empty space"""
        
        empty_spaces = {}
        
        i = 0
        
        while i < len(sud):
            
            j = 0

            while j < len(sud[0]):

                if sud[i][j] == 0:

                    empty_spaces[(i, j)] = possible_values(sud, i, j)
                    
                j += 1
            
            i += 1
            
        return empty_spaces
    
    def possible_values(sud, row, col):
        """Takes in a row-col pair and generates possible candidates following sudoku constraints"""
        
        poss_row_vals = [i for i in range(1, 10) if i not in sud[row]]
                    
        poss_col_vals = [i for i in range(1, 10) if i not in sud[:,col]]
        
        subgrid = get_subgrid(sud, row, col)
        
        poss_subgrid_vals = [i for i in range(1, 10) if i not in subgrid]
        
        possible_values = list(set(poss_subgrid_vals).intersection(poss_row_vals, poss_col_vals))
        
        return possible_values
    

    def check_valid_candidates(sud, empty_spaces):
        """If same single candidate for two or more squares in the same row, column or subgrid, sets valid_candidates to false
           If value empty, sets to false also"""
        
        single_vals = [[],[],[],[],[],[],[],[],[]]
        
        for k, v in empty_spaces.items():
            
            if len(v) == 1:
            
                val = v[0]
        
                for tup in single_vals[val - 1]:
                    
                    if tup[0] == k[0] or tup[1] == k[1] or np.array_equiv(get_subgrid(sud,tup[0],tup[1]), get_subgrid(sud,k[0],k[1])) == True:
    
                        return False
                    
                single_vals[val - 1].append(k)
                    
            elif len(v) == 0:
                
                return False
                
        return True
    
    def set_value(sud, empty_spaces, row, col, num):
        """Sets chosen value of square and updates empty spaces dictionary """
            
        sudoku_copy = copy.deepcopy(sud)

        sudoku_copy[row][col] = num

        empty_spaces_new = update_empty_spaces(sudoku_copy, empty_spaces, row, col)
        
        # check if both dict is valid and grid is valid
        valid = check_valid_candidates(sudoku_copy, empty_spaces_new) and is_valid_grid(sudoku_copy)
        
        return sudoku_copy, empty_spaces_new, valid
    
    def update_empty_spaces(sud, empty_spaces, row, col):
        """Updates empty_spaces dictionary"""
        
        subgrid = get_subgrid(sud, row, col)
        subgrid_coord = get_subgrid_coordinates(row, col)
        
        # remove item from dict
        del empty_spaces[(row, col)]
        
        # update only affected values
        for k in empty_spaces:
    
            curr_row, curr_col = k
            
            curr_subgrid = get_subgrid(sud, curr_row, curr_col)
            
            if k[0] == row or k[1] == col:
      
                empty_spaces[k] = possible_values(sud, curr_row, curr_col)
            
            elif k[0] in range(subgrid_coord[0], subgrid_coord[1]) and k[1] in range(subgrid_coord[2], subgrid_coord[3]):
      
                empty_spaces[k] = possible_values(sud, curr_row, curr_col)
        
        return empty_spaces
        
    def get_subgrid(sud, row, col):
        """Returns subgrid containing row-col pair"""

        subgrid_y = (col // 3) * 3
        
        subgrid_x = (row // 3) * 3
        
        subgrid = sud[subgrid_x : subgrid_x + 3, subgrid_y : subgrid_y + 3]
        
        return subgrid
    
    def get_subgrid_coordinates(row, col):
        """Returns subgrid coordinates containing row-col pair"""
        
        subgrid_y = (col // 3) * 3
        
        subgrid_x = (row // 3) * 3
        
        return [subgrid_x, subgrid_x + 3, subgrid_y, subgrid_y + 3]
        
    def check_allowed_numbers(sud):
        """Checks if sudoku contains allowed numbers from 1 to 9. Returns a boolean.
           Only used at start in the event an invalid sudoku is given"""
        
        allowed_numbers = [x for x in range(0, 10)]
        
        i = 0
        
        while i < len(sud):
            
            j = 0
            
            while j < len(sud[0]):
                
                if sud[i][j] not in allowed_numbers:
                    
                    return False
                
                j += 1
            
            i += 1
                
        return True
    
    def check_unique_numbers(sud):
        """Checks if numbers in rows, columns and subgrids are all unique if not equal to 0"""
        
        for row in sud:
            
            row_nums = [x for x in row if x != 0]
            
            if len(set(row_nums)) < len(row_nums):
                
                return False
            
        
        for col in sud.T:
            
            col_nums = [y for y in col if y != 0]

            if len(set(col_nums)) < len(col_nums):
          
                return False

            
        subgrid_x = 0
        
        while subgrid_x <= 9:
            
            subgrid_y = 0
            
            while subgrid_y <= 9:
                
                subgrid = sud[subgrid_x : subgrid_x + 3, subgrid_y : subgrid_y + 3].flatten()
                
                subgrid_nums = [z for z in subgrid if z != 0]
            
                if len(set(subgrid_nums)) < len(subgrid_nums):
                 
                    return False
                
                subgrid_y += 3
                
            subgrid_x += 3
            
        return True
    
    def choose_square_to_update(empty_spaces):
        """Picks next square to update on basis of having least number of candidates"""
        
        len_list = [(len(empty_spaces[space]), space) for space in empty_spaces.keys()]
        
        min_tup = min(len_list)
        
        return min_tup[1]
    
    def narrow_values(empty_spaces, row, col):
        """Compared possible values in the same subgrid, row and column and whittles them down, removing possibilities
           Utilises several sudoku strategies"""
        
        subgrid_coord = get_subgrid_coordinates(row, col)
        list_of_spaces_subgrid = []
        list_of_values_subgrid = []
        list_of_spaces_row = []
        list_of_values_row = []
        list_of_spaces_col = []
        list_of_values_col = []
        
        # list of singleton values - used to eliminate value if crops up as a possible candidate for another position
        list_of_singles = []
        
        for k, v in empty_spaces.items():
            
            curr_row, curr_col = k
            
            if curr_row in range(subgrid_coord[0], subgrid_coord[1]) and curr_col in range(subgrid_coord[2], subgrid_coord[3]):
                
                list_of_spaces_subgrid.append(k)
                list_of_values_subgrid.append(v)

                if len(v) == 1:
                    
                    if (k,v) not in list_of_singles:
                        
                        list_of_singles.append((k,v, "g"))
                
            if curr_row == row:
                
                list_of_spaces_row.append(k)
                list_of_values_row.append(v)

                if len(v) == 1:
                    
                    if (k,v) not in list_of_singles:
                        
                        list_of_singles.append((k,v, "r"))
                
            if curr_col == col:
                
                list_of_spaces_col.append(k)
                list_of_values_col.append(v)

                if len(v) == 1:
                    
                    if (k,v) not in list_of_singles:
                        
                        list_of_singles.append((k,v, "c"))
        
        # collate counts of appearances of values in current row, col and subgrid
        num_count_subgrid = [0,0,0,0,0,0,0,0,0]
        num_count_row = [0,0,0,0,0,0,0,0,0]
        num_count_col = [0,0,0,0,0,0,0,0,0]
            
        i = 0
            
        while i < len(list_of_values_subgrid):
                
            j = 0
                
            while j < len(list_of_values_subgrid[i]):
                
                curr_num = list_of_values_subgrid[i][j]
                
                num_count_subgrid[curr_num - 1] += 1
                
                j +=1
            
            i += 1
            
        i = 0
        
        while i < len(list_of_values_row):
                
            j = 0
                
            while j < len(list_of_values_row[i]):
                
                curr_num = list_of_values_row[i][j]
                
                num_count_row[curr_num - 1] += 1
                
                j +=1
            
            i += 1
            
        i = 0
        
        while i < len(list_of_values_col):
                
            j = 0
                
            while j < len(list_of_values_col[i]):
                
                curr_num = list_of_values_col[i][j]
                
                num_count_col[curr_num - 1] += 1
                
                j +=1
            
            i += 1  
            

        # block of code checks for singleton values and then checks for its appearance in other possible candidates
        # for spaces in the same row, column or subgrid
        # if found, deleted from the possible candidates
        for tup in list_of_singles:

            if tup[2] == "g":

                for i, arr in enumerate(list_of_values_subgrid):
          
                    if tup[1][0] in arr:

                        update_k = list_of_spaces_subgrid[i]
                    
                        single = np.array([tup[1][0]])

                        if update_k != tup[0]:

                            arr = empty_spaces[update_k]
                            # use set difference to remove value from possible candidates
                            empty_spaces[update_k] = np.setdiff1d(arr,single,True)

            elif tup[2] == "c":

                for i, arr in enumerate(list_of_values_col):

                    if tup[1][0] in arr:

                        update_k = list_of_spaces_col[i]
                            
                        single = np.array([tup[1][0]])

                        if update_k != tup[0]:

                            arr = empty_spaces[update_k]
                            empty_spaces[update_k] = np.setdiff1d(arr,single,True)

            elif tup[2] == "r":

                for i, arr in enumerate(list_of_values_row):
   
                    if tup[1][0] in arr:

                        update_k = list_of_spaces_row[i]
    
                        single = np.array([tup[1][0]])

                        if update_k != tup[0]:

                            arr = empty_spaces[update_k]
                            empty_spaces[update_k] = np.setdiff1d(arr,single,True)

        # block of code has 2 functions:
        # 1) identifies single instances of a value in a row, column and subgrid for the square - if so, narrows down possible
        #    candidates to the one value
        # 2) identifies instances of paired values for 2 squares - if 2 squares contain the same pair of values in a row, column
        #    or subgrid, possible candidates are narrowed down to that pair
        
        pair_subgrid = []
        
        for index, count in enumerate(num_count_subgrid):
            
            if count == 1:
                
                for i, arr in enumerate(list_of_values_subgrid):
                    
                    if (index + 1) in arr:
                        
                        empty_spaces[list_of_spaces_subgrid[i]] = np.array([index + 1])
                        
            if count == 2:
                
                pair_subgrid.append(index + 1)
                
        if len(pair_subgrid) == 2:
            
            for i, arr in enumerate(list_of_values_subgrid):
                
                if len(empty_spaces[list_of_spaces_subgrid[i]]) > 1:
                    
                    if pair_subgrid[0] in arr and pair_subgrid[1] in arr:
                    
                        empty_spaces[list_of_spaces_subgrid[i]] = np.array([pair_subgrid[0], pair_subgrid[1]])
                    
        pair_row = []     
        for index, count in enumerate(num_count_row):
            
            if count == 1:
                
                for i, arr in enumerate(list_of_values_row):
                    
                    if (index + 1) in arr:
                        
                        empty_spaces[list_of_spaces_row[i]] = np.array([index + 1])
                        
            if count == 2:
                
                pair_row.append(index + 1)
                
        if len(pair_row) == 2:
            
            for i, arr in enumerate(list_of_values_row):
                
                if len(empty_spaces[list_of_spaces_row[i]]) > 1:
                    
                    if pair_row[0] in arr and pair_row[1] in arr:
                    
                        empty_spaces[list_of_spaces_row[i]] = np.array([pair_row[0], pair_row[1]])
                    
        pair_col = []
                        
        for index, count in enumerate(num_count_col):
            
            if count == 1:
                
                for i, arr in enumerate(list_of_values_col):
                    
                    if (index + 1) in arr:
                        
                        empty_spaces[list_of_spaces_col[i]] = np.array([index + 1])
                        
            if count == 2:
                
                pair_col.append(index + 1)
                
        if len(pair_col) == 2:
            # 2 squares with same pair of numbers -> can narrow down to these 2 possibilities for both squares
            
            for i, arr in enumerate(list_of_values_col):
                
                if len(empty_spaces[list_of_spaces_col[i]]) > 1:
                    
                    if pair_col[0] in arr and pair_col[1] in arr:
                    
                        empty_spaces[list_of_spaces_col[i]] = np.array([pair_col[0], pair_col[1]])
                                    
        return empty_spaces
        
    def narrow_start(sud, empty_spaces):
        """Narrows down intial dictionary"""
        
        i = 0
        
        while i < len(sud):
            
            empty_spaces = narrow_values(empty_spaces, i, i)
            
            i += 1
                
        return empty_spaces
                
    def is_valid_grid(sud):
        """Checks if current grid is valid"""
            
        return check_unique_numbers(sud)
        
    def is_goal(sud):
        """Checks if goal has been reached"""
            
        # first checks if grid contains zeros
        for row in sud:
                
            if 0 in row:
                    
                return False
            
        for col in sud.T:
                
            if 0 in col:
                    
                return False
                
        # then checks if all values in rows, columns and subgrids are unique
            
        return check_unique_numbers(sud)
    
    def dfs(sud):
        """Backtracking algorithm for sudoku"""
        
        # generate initial candidates
        empty_spaces = generate_initial_dict(sud)
            
        return helper(sud, empty_spaces)
    
    def helper(sudoku, empty_spaces):
        """Helper function for depth-first search"""

        # if sudoku is complete, return sudoku
        if is_goal(sudoku) == True:
            
            return sudoku

        
        # select unassigned square
        row, col = choose_square_to_update(empty_spaces)

        # for each candidate for square
        for num in empty_spaces[(row, col)]:

            # deduce resulting grid, dictionary and whether grid and dict are valid
            empty_spaces_copy = copy.deepcopy(empty_spaces)
            next_step, empty_spaces_new, valid = set_value(sudoku, empty_spaces_copy, row, col, num)

            if valid == True:

                # narrow candidate values down using sudoku solving strategies
                empty_spaces_new = narrow_values(empty_spaces_new, row, col)


                # recursive call to helper function
                result = helper(next_step, empty_spaces_new)

                # if output is not a fail, return result
                if np.array_equiv(result, np.ones((9,9)) * -1) == False:

                    return result


        return np.ones((9,9)) * -1

# run the solver and return the result
    solved_sudoku = dfs(sudoku)

    return solved_sudoku
