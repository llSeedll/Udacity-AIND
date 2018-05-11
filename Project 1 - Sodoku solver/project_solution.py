assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]

col_units = [cross(rows, c) for c in cols]

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

unitlist = row_units + col_units + square_units

diagonals_added = False

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

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

def add_diag_constraint():
    global diagonals_added, unitlist
    if not diagonals_added :
        diagonal_units_1 = [r+c for r,c in zip(rows,cols)]
        diagonal_units_2 = [r+c for r,c in zip(rows, cols[::-1])]
        #diagonal_units_1 = [v+c for s,v in enumerate(rows) for r,c in enumerate(cols) if s==r]
        #diagonal_units_2 = [v+c for s,v in enumerate(rows) for r,c in enumerate(cols[::-1]) if s==r]
        diagonal_units = [diagonal_units_1]+[diagonal_units_2]
        unitlist = unitlist + diagonal_units
        diagonals_added = True
    pass

def x_wing(values):
    checked_boxes = []
    x_wings_indices = {}
    indices = dict((s, [i for i,v in enumerate(rows) if rows[i]==s][0]) for s in rows)
    row_wings = [(r1v, [r1,r2]) for r1 in boxes for r2 in row_units[indices[r1[0]]] for r1v in values[r1] for r2v in values[r2] if r1!=r2 and r1v==r2v  and len([ru for ru in row_units[indices[r1[0]]] if r1v in values[ru]])==2  ]
    [checked_boxes.append((w1, w2)) for (w1, w2) in row_wings if (w1, w2) not in checked_boxes and (w2, w1) not in checked_boxes]
    
    for (v,t) in checked_boxes:
        for (v2, t2) in checked_boxes:
            if t!=t2 and v==v2 and t[0][1]==t2[0][1] and t[1][1]==t2[1][1]:
                if v not in x_wings_indices:
                    x_wings_indices[v] = [t[0], t[1], t2[0], t2[1]]      
    
    columns = []
    for value in x_wings_indices:
        cols_u = []
        [cols_u.append(c[1]) for c in x_wings_indices[value] if c[1] not in cols_u]
        [columns.append((value, b)) for cu in cols_u for b in col_units[int(cu)-1] if cu==b[1] and value in values[b] and b not in columns and b not in x_wings_indices[value]]
    
    [assign_value(values, p, values[p].replace(v, "")) for (v,p) in columns ]
    
    #print(x_wings_indices)
    
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Do you need me do you think Im crazy
    # oh i think that i found myself a cheerleader, she's always right there when I need her
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    checked_boxes = []
    for b in boxes:
        checked_boxes.append(b)
        nt_list = [ (b,b2) for b2 in peers[b] if len(values[b2])==2 and values[b]==values[b2] and b2 not in checked_boxes]
        for n in [nt for nt in nt_list if len(nt)>0]:
            if n[0][0]==n[1][0]: # same row
                index = [i for i,v in enumerate(rows) if rows[i]==n[0][0]][0]
                for v in values[b]:
                    [assign_value(values, l, values[l].replace(v, "")) for l in [vv for i,vv in enumerate(row_units[index]) if vv!=n[0] and vv!=n[1] ]]
            if n[0][1]==n[1][1]: # same column
                index = [i for i,v in enumerate(cols) if cols[i]==n[0][1]][0]
                for v in values[b]:
                    [assign_value(values, l, values[l].replace(v, "")) for l in [vv for i,vv in enumerate(col_units[index]) if vv!=n[0] and vv!=n[1] ]]
            sus = [i for i,v in enumerate(square_units) if n[0] in square_units[i] and n[1] in square_units[i]]
            if len(sus)>0: # same squared unit
                index = [i for i,v in enumerate(square_units[sus[0]]) if square_units[sus[0]][i]==n[0]][0]
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

def eliminate(values):
    v = dict()
    v = [(e,values[e]) for e in values if len(values[e])==1]
    for (e,ve) in v:
        for p in peers[e]:
            #values[p] = values[p].replace(values[e], "")
            assign_value(values, p, values[p].replace(values[e], ""))
    return values

def only_choice(values):
    for u in unitlist:
        tmp = dict()
        for b in u:
            for e in values[b]:
                if e not in tmp:
                   tmp[e] = {'o':1, 'pos':[b]}
                else:
                    tmp[e]['o'] += 1
                    tmp[e]['pos'].append(b)
        for p in tmp:
            if tmp[p]['o']==1 :
                #values[tmp[p]['pos'][0]] = p
                assign_value(values, tmp[p]['pos'][0], p)
    return values

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

def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    if len([box for box in values.keys() if len(values[box])==1])==len(values):
        return values
    key = sorted([v for v in values.items() if len(v[1])>1], key=lambda x:len(x[1]))[0]
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
    if not isinstance(grid, dict) :
        values = grid_values(grid)
    assignments.append(values.copy())
    add_diag_constraint()
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #assignments.append(grid_values('.................................................................................'))
    #display(solve(diag_sudoku_grid)) 
    x_wing_grid = reduce_puzzle(grid_values('67941.352248.957.1153762984......42.7...8.536......17.5871296434618.72.53.2.54817'))
    display(x_wing_grid)
    display(x_wing(x_wing_grid))
    
    print("")
    x_wing_grid = reduce_puzzle(grid_values('329148657158763.2.6472..318.3167..8.78.3.15.6.968..73181.437.6..6..82173.73.168..'))
    display(x_wing_grid)
    display(x_wing(x_wing_grid))
    
    
    try:
        from visualize import visualize_assignments
        #visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


"""
    before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
    possible_solutions_1 = [
        {'G7': '6', 'G6': '3', 'G5': '2', 'G4': '9', 'G3': '1', 'G2': '8', 'G1': '7', 'G9': '5', 'G8': '4', 'C9': '1',
         'C8': '5', 'C3': '8', 'C2': '237', 'C1': '23', 'C7': '9', 'C6': '6', 'C5': '37', 'A4': '2357', 'A9': '8',
         'A8': '6', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'F6': '125', 'F7': '35', 'F8': '9',
         'F9': '7', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'C4': '4',
         'B8': '3', 'B9': '4', 'I9': '9', 'I8': '7', 'I1': '23', 'I3': '23', 'I2': '6', 'I5': '5', 'I4': '8', 'I7': '1',
         'I6': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'E8': '1', 'A7': '27', 'A6': '257', 'E5': '347',
         'E4': '6', 'E7': '345', 'E6': '579', 'E1': '8', 'E3': '79', 'E2': '37', 'H8': '2', 'H9': '3', 'H2': '9',
         'H3': '5', 'H1': '4', 'H6': '17', 'H7': '8', 'H4': '17', 'H5': '6', 'D8': '8', 'D9': '6', 'D6': '279',
         'D7': '34', 'D4': '237', 'D5': '347', 'D2': '1', 'D3': '79', 'D1': '5'},
        {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8', 'H5': '6', 'F9': '7',
         'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8', 'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23',
         'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5', 'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9',
         'A4': '2357', 'A7': '27', 'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
         'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2', 'F6': '125',
         'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '79', 'F1': '6', 'F2': '4', 'F3': '23', 'F4': '1235',
         'F5': '8', 'E2': '3', 'F7': '35', 'F8': '9', 'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17',
         'D3': '79', 'B4': '27', 'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6',
         'D6': '279', 'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}
        ]

    
    before_naked_twins_2 = {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9',
                            'A9': '1', 'B1': '6', 'B2': '9', 'B3': '8', 'B4': '4', 'B5': '37', 'B6': '1', 'B7': '237',
                            'B8': '5', 'B9': '237', 'C1': '23', 'C2': '5', 'C3': '1', 'C4': '23', 'C5': '379',
                            'C6': '2379', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8', 'D2': '17', 'D3': '9',
                            'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
                            'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9',
                            'F1': '4', 'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6',
                            'F8': '8', 'F9': '257', 'G1': '1', 'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345',
                            'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7', 'H2': '2', 'H3': '4', 'H4': '9',
                            'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3', 'I3': '5',
                            'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'}

    possible_solutions_2 = [
        {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9', 'A9': '1', 'B1': '6',
         'B2': '9', 'B3': '8', 'B4': '4', 'B5': '37', 'B6': '1', 'B7': '237', 'B8': '5', 'B9': '237', 'C1': '23',
         'C2': '5', 'C3': '1', 'C4': '23', 'C5': '79', 'C6': '79', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8',
         'D2': '17', 'D3': '9', 'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
         'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9', 'F1': '4',
         'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6', 'F8': '8', 'F9': '257', 'G1': '1',
         'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345', 'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7',
         'H2': '2', 'H3': '4', 'H4': '9', 'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3',
         'I3': '5', 'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'},
        {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9', 'A9': '1', 'B1': '6',
         'B2': '9', 'B3': '8', 'B4': '4', 'B5': '3', 'B6': '1', 'B7': '237', 'B8': '5', 'B9': '237', 'C1': '23',
         'C2': '5', 'C3': '1', 'C4': '23', 'C5': '79', 'C6': '79', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8',
         'D2': '17', 'D3': '9', 'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
         'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9', 'F1': '4',
         'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6', 'F8': '8', 'F9': '257', 'G1': '1',
         'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345', 'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7',
         'H2': '2', 'H3': '4', 'H4': '9', 'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3',
         'I3': '5', 'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'}
    ]

    #display(diag_constraint(diag_sudoku_grid))
    display(before_naked_twins_1)
    print("")
    display(naked_twins(before_naked_twins_1))
    print("")
    display(possible_solutions_1[0])
    print("")
    display(possible_solutions_1[1])
"""