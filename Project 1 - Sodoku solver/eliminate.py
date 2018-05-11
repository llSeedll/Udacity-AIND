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
    
g = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')

display(eliminate(g))