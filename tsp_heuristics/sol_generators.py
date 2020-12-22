# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 08:56:55 2020

@author: dakar
"""

import random

def random_tour_list(tsp):
        '''
        Make a random tour (permutation) of the nodes in the TSP
        
        Parameters
        ----------
        tsp : TSP
            The tsp object we want to make the tour from.
        
        Returns
        -------
        tour_list : list
            The list of node visits in this tour; doesn't loop back to starting node.
        '''

        tour = random.sample(tsp.nodes,len(tsp.nodes))
        return(tour)
    
    
def ordered_tour_list(tsp,ordered_list=None):
    '''
    Return a list of the nodes in the TSP as they are.
    
    Simply converts tsp.nodes into a list
    
    Parameters
    ----------
    tsp : TSP
        The tsp object we want to make the tour from.
    ordered_list : iterable
        The nodes in the order we want for the tour; don't include the return to start.
        Must be contain all nodes in tsp.nodes and be the same length. If none
        defaults to list(tsp.nodes)

    Returns
    -------
    tour_list : list
        The list of node visits in this tour; doesn't loop back to starting node.
    '''
    
    default_order = list(tsp.nodes)
    
    if ordered_list is None:
        ordered_list = default_order
    # check to make sure provided order is same size and contain same elements as tsp.nodes
    elif len(tsp.nodes.difference(ordered_list)) > 0 or len(set(ordered_list).difference(tsp.nodes)) > 0:
        ordered_list = default_order
    return(ordered_list)

def greedy_tour_list(tsp,start_node=None):
    '''
    Return a tour starting at start_node that uses the best possible edge
    
    From the starting node, find the closest node and continue to add the closest
    node successively. If, not provided (or a valid node in the TSP), start_node defaults to a random node
    
    Parameters
    ----------
    start_node : node in tsp.nodes
        The node to begin the greedy search from. If None, set to random.choice(tsp.nodes)

    Returns
    -------
    tour_list : list
        The list of node visits in this tour; doesn't loop back to starting node.
    '''
    
    if start_node not in tsp.nodes:
        start_node = random.choice(tsp.nodes)
        
    tour_list = list(start_node)
        
    non_visited_nodes = tsp.nodes.remove(start_node)
    
    # recursively add the next best node from the current node
    while len(non_visited_nodes) > 0:
        best_dist = None
        best_node = None
        poss_edge_dict = tsp.dist_dod[tour_list[-1]]
        
        # loop through non_visited_nodes and find first node with smallest distance
        for node in non_visited_nodes:
            if best_dist == None:
                best_dist = poss_edge_dict[node]
                best_node = node
            elif poss_edge_dict[node] < best_dist:
                best_dist = poss_edge_dict[node]
                best_node = node
                
        # add best node to tour and remove from non_visited_nodes to prevent subtours
        tour_list.append(best_node)
        non_visited_nodes.remove(best_node)
    return(tour_list)