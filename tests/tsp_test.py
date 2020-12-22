# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 15:57:33 2020

@author: dakar
"""

import tsp_heuristics as th



#%% TSP Test
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
    
print('Adding nodes')

print('Adding with no distances')
tsp1.add_nodes({'new_node1':{}},default=47)
print(tsp1.nodes)
print(tsp1.dist_dod)

print('Adding with distances')
tsp1.add_nodes({'new_node2':{node:13 for node in tsp1.nodes}})
print(tsp1.nodes)
print(tsp1.dist_dod)


print('Updating dist_dod')
# change all distances from new_node1 to 50
# all distances to new_node1 to 100
tsp1.add_nodes({**{'new_node1':{node:50 for node in tsp1.nodes.difference(set(['new_node1']))}},
                **{node:{'new_node1':100} for node in tsp1.nodes.difference(set(['new_node1']))}})
print(tsp1.dist_dod['new_node1'])
print({node:tsp1.dist_dod[node]['new_node1']
       for node in tsp1.nodes.difference(set(['new_node1']))})


#%% Tour Tests
random_tour = th.TSPTour.from_tsp(tsp1,'random')
ordered_tour = th.TSPTour.from_tsp(tsp1,'ordered')
greedy_tour = th.TSPTour.from_tsp(tsp1,'greedy')

print(random_tour)
# random_tour.n_swap(0)
for n in range(2,len(random_tour.tour_list)+1):
    random_tour.n_swap(n)
    print('n: {} \nnew_tour: {} \n'.format(n,random_tour))
    print()
