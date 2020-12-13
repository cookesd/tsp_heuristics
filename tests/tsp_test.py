# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:57:33 2020

@author: dakar
"""

import tsp_heuristics as th

my_dod = {0:{1:47,2:13},1:{0:47,2:50},2:{0:13,1:50}}
tsp1 = th.TSP(incoming_data = my_dod)
print(tsp1.nodes)
print(tsp1.dist_dod)

print('Number of nodes: {}'.format(len(tsp1)))

print('Iterating through nodes')
for node in tsp1:
    print(node)
    
print('Enumerating nodes')
for i,node in enumerate(tsp1):
    print('Node {} is {}'.format(i+1,node))