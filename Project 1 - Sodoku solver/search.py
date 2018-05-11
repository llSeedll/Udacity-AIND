# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 01:25:46 2017

@author: Aboubacar Diallo
"""

from utils import *

def grid_values(grid):
    dictionary = dict()
    i = 0
    for b in boxes:
        dictionary[b] = grid[i]=='.' and '123456789' or grid[i]
        i+=1
    return dictionary
"""        
display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))
"""
def eliminate(values):
    v = dict()
    for e in values:
        if len(values[e])==1:
            v[e] = values[e]
    for e in v:
        for p in peers[e]:
            values[p] = values[p].replace(values[e], "")
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
                values[tmp[p]['pos'][0]] = p
    return values
"""
        for b in u:
            if len(values[b])==1:
                continue
            for e in b:
                if (e not in values[p] for p in peers[b]):
                    values[b] = e
"""

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
 
g = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
g1 = grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')

"""
e = eliminate(g)

display(e)


display(only_choice(eliminate(only_choice(e))))
display(reduce_puzzle(g))
search(g1)
"""

display(search(g1))