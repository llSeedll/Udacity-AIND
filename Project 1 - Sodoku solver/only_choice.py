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
            
    
g = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')

e = eliminate(g)

display(e)


display(only_choice(eliminate(only_choice(e))))