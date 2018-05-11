assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# boxes' coordinates
boxes = cross(rows, cols)
# list of row units with column coordinates
row_units = [cross(r, cols) for r in rows]
# list of colunmn units with row coordinates 
col_units = [cross(rows, c) for c in cols]
# list of square units
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# list of all units
unitlist = row_units + col_units + square_units
# checks for diagonal constraints presense
diagonals_added = False

# dictionary of units per box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# dictionary of peers per box
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

# assigns value to box and adds it to assignments variable, used for the display with pygame
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# adds two new units for the diagoonal constraints
def add_diag_constraint():
    global diagonals_added, unitlist, units, peers
    if not diagonals_added :
        diagonal_units_1 = [r+c for r,c in zip(rows,cols)]
        diagonal_units_2 = [r+c for r,c in zip(rows, cols[::-1])]
        diagonal_units = [diagonal_units_1]+[diagonal_units_2]
        unitlist = unitlist + diagonal_units
        units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
        peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)
        diagonals_added = True
    pass

# cross reference of 4 boxes that contain a same possible value. it eliminates
# that possible value from some of the other boxes following some constraints (same row or same column) depending
# on the algorithm. The 4 boxes must form a loop on the grid(rectangle)
def x_wing(values):
    checked_boxes = []
    x_wings_indices = {}
    # all row indices indexed from A to I
    indices = dict((s, [i for i,v in enumerate(rows) if rows[i]==s][0]) for s in rows)
    # find all pairs in the same row that contain one of same possible values
    row_wings = [(r1v, [r1,r2]) for r1 in boxes for r2 in row_units[indices[r1[0]]] for r1v in values[r1] for r2v in values[r2] if r1!=r2 and r1v==r2v  and len([ru for ru in row_units[indices[r1[0]]] if r1v in values[ru]])==2  ]
    # unique list of previous found pairs
    [checked_boxes.append((w1, w2)) for (w1, w2) in row_wings if (w1, w2) not in checked_boxes and (w2, w1) not in checked_boxes]
    
    # check if pairs share the same columns
    for (v,t) in checked_boxes:
        for (v2, t2) in checked_boxes:
            if t!=t2 and v==v2 and t[0][1]==t2[0][1] and t[1][1]==t2[1][1]:
                if v not in x_wings_indices:
                    x_wings_indices[v] = [t[0], t[1], t2[0], t2[1]]      
    
    # retrieve boxes in given column that contain a possile value to remove
    columns = []
    for value in x_wings_indices:
        cols_u = []
        [cols_u.append(c[1]) for c in x_wings_indices[value] if c[1] not in cols_u]
        [columns.append((value, b)) for cu in cols_u for b in col_units[int(cu)-1] if cu==b[1] and value in values[b] and b not in columns and b not in x_wings_indices[value]]
    
    # remove possible values from previously retrieved boxes
    [assign_value(values, p, values[p].replace(v, "")) for (v,p) in columns ]
    
    return values

# finds two boxes who are peers and share the same two possible values. Then 
# removes those two values from the peers unit the boxes share
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    checked_boxes = []
    # iterate through all boxes to find naked twins
    for b in boxes:
        checked_boxes.append(b)
        # list of all naked twins
        nt_list = [ (b,b2) for b2 in peers[b] if len(values[b2])==2 and values[b]==values[b2] and b2 not in checked_boxes]
        # iterate through the naked twins list to remove possible values from peers
        for n in [nt for nt in nt_list if len(nt)>0]:
            if n[0][0]==n[1][0]: # same row
                index = [i for i,v in enumerate(rows) if rows[i]==n[0][0]][0]
                for v in values[b]:
                    [assign_value(values, l, values[l].replace(v, "")) for l in [vv for i,vv in enumerate(row_units[index]) if vv!=n[0] and vv!=n[1] ]]
            elif n[0][1]==n[1][1]: # same column
                index = [i for i,v in enumerate(cols) if cols[i]==n[0][1]][0]
                for v in values[b]:
                    [assign_value(values, l, values[l].replace(v, "")) for l in [vv for i,vv in enumerate(col_units[index]) if vv!=n[0] and vv!=n[1] ]]
            
            sus = [i for i,v in enumerate(square_units) if n[0] in square_units[i] and n[1] in square_units[i]]
            if len(sus)>0: # same square unit
                for v in values[b]:
                    [assign_value(values, l, values[l].replace(v, "")) for l in [vv for i,vv in enumerate(square_units[sus[0]]) if vv!=n[0] and vv!=n[1] ]]
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    dictionary = dict()
    i = 0
    for b in boxes:
        dictionary[b] = grid[i]=='.' and '123456789' or grid[i]
        i+=1
    return dictionary

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

# eliminates possible values from peers of already assigned boxes
def eliminate(values):
    v = dict()
    v = [(e,values[e]) for e in values if len(values[e])==1]
    for (e,ve) in v:
        for p in peers[e]:
            assign_value(values, p, values[p].replace(values[e], ""))
    return values

# if a possible value is only present in one box for a unit, it is assigned to 
# that box
def only_choice(values):
    # find unique occurrence of possible values in each unit
    for u in unitlist:
        tmp = dict()
        for b in u:
            for e in values[b]:
                if e not in tmp:
                   tmp[e] = {'o':1, 'pos':[b]}
                else:
                    tmp[e]['o'] += 1
                    tmp[e]['pos'].append(b)
        # assign unique occurrences to their respective boxes
        for p in tmp:
            if tmp[p]['o']==1 :
                assign_value(values, tmp[p]['pos'][0], p)
    return values

# applies only_choice and eliminate to the grid until there's nothing more to do
# with the given constraints
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len ([box for box in values.keys() if len(values[box]) == 1])
        values = only_choice(eliminate(values))
        solved_values_after = len ([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box])==0]):
            return False
    return values

# implements a depth first search algorithm to find a possible solution
def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    # when all boxes have a single value assigned to them a solution has been found
    if len([box for box in values.keys() if len(values[box])==1])==len(values):
        return values
    # sort keys with respect to the number of possible values and retrieve the box with
    # the least possible values
    key = sorted([v for v in values.items() if len(v[1])>1], key=lambda x:len(x[1]))[0]
    # for every possible value (key[1]) in the box previously found(key[0]), we attempt to find
    # a solution by assigning those values to the box, creating nodes for the
    # DFS tree
    for c in key[1]:
        tmp = values.copy()
        tmp[key[0]] = c
        sv = search(tmp)
        if sv!=False:
            return sv
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid
    # in case the grid is not a dictionary, it is transformed into one and attempted to solve
    if not isinstance(grid, dict) :
        values = grid_values(grid)
    assignments.append(values.copy())
    add_diag_constraint()
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    g = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))
    #display(solve(g))
    
    try:
        from visualize import visualize_assignments
        #visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
