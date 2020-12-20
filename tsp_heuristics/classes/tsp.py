# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 12:12:13 2020

@author: dakar
"""


#%%
import warnings
import random
from tsp_heuristics.io.read_data import make_tsp

class TSP(object):
    def __init__(self,incoming_data=None):
        
        self.dist_dod = dict()
        self.nodes = set()
        
        # call a function to determine what format the data is in
        # then fill the dist_dod and nodes parameters accordingly
        if incoming_data is not None:
            make_tsp(incoming_data,obj_to_use = self)
            
    def __str__(self):
        return 'this is the string representation'
    
    def __iter__(self):
        '''
        Iterates through nodes in the TSP problem

        Yields
        -------
        nodes.

        '''
        for node in self.nodes:
            yield(node)
            
    def __len__(self):
        '''
        Number of nodes in the TSP problem
        '''
        return(len(self.nodes))
        
        
    def _get_updated_node_dist_dict_for(self,new_nodes,orig_nodes,node_dist_dict,default=0):
        '''
        Takes the provided node_dist_dict and makes sure new nodes have to and from distances
        
        For the new nodes, it makes sure they have from and to distances, using
        the symmetric value if present or the default. Then loops through the original
        nodes from the object and makes sure there are distances to all the new nodes.
        Keeps all provided distances between original nodes and doesn't update the
        non-provided symmetric part. This function provides user warnings of
        missing distances and tells whether using symmetric or default value.

        Parameters
        ----------
        new_nodes : set
            Nodes being added to the TSP from this step.
        orig_nodes : set
            Nodes that were already in the TSP.
        node_dist_dict : dict of dicts
            Outer keys are new and original nodes. Inner keys are other nodes besides this outer node.
            Inner values are the distances
        default : numeric, optional
            The value to use when a required distance doesn't exist and the
            symmetric value doesn't exist. The default is 0.

        Returns
        -------
        new_node_dist_dict : dict of dicts
            The updated node_dist_dict with all required distances between new
            nodes and existing nodes.

        '''
        missing_distances = {}
        new_node_dist_dict = {node:{} for node in orig_nodes.union(new_nodes)}
        for new_node in new_nodes:
            symmetric_replacements = []
            default_replacements = []
            for other_node in new_nodes.union(orig_nodes).difference(set([new_node])):
                if other_node in node_dist_dict[new_node].keys():
                    new_node_dist_dict[new_node][other_node] = node_dist_dict[new_node][other_node]
                elif other_node in node_dist_dict.keys():
                    if new_node in node_dist_dict[other_node].keys():
                        new_node_dist_dict[new_node][other_node] = node_dist_dict[other_node][new_node]
                        symmetric_replacements.append(other_node)
                    else:
                        new_node_dist_dict[new_node][other_node] = default
                        default_replacements.append(other_node)
                else:
                    new_node_dist_dict[new_node][other_node] = default
                    default_replacements.append(other_node)
            if len(symmetric_replacements) > 0 or len(default_replacements) > 0:
                msg = 'New node ({}) missing distances'.format(new_node)
                if len(symmetric_replacements) > 0:
                    msg = '\n\t'.join([msg,
                                       'distances to nodes ({}) replaced with symmetric distance'
                                       .format(', '.join([str(i) for i in symmetric_replacements]))])
                if len(default_replacements) > 0:
                    msg = '\n\t'.join([msg,
                                       'distances to nodes ({}) replaced with default ({}) distance'
                                       .format(', '.join([str(i) for i in default_replacements]),
                                               default)])
                    
                missing_distances[new_node] = msg
        # distances for original nodes
        # keep any existing distances
        # and go through all the new nodes that aren't already listed and use
        # the symmetric distance or default
        for orig_node in orig_nodes:
            symmetric_replacements = []
            default_replacements = []
            if orig_node in node_dist_dict.keys():
                new_node_dist_dict[orig_node] = node_dist_dict[orig_node]
            else:
                new_node_dist_dict[orig_node] = {}
            # use either symmetric or default distance for new nodes not listed
            for new_node in new_nodes.difference(set(new_node_dist_dict[orig_node].keys())):
                if orig_node in node_dist_dict[new_node].keys():
                    new_node_dist_dict[orig_node][new_node] = node_dist_dict[new_node][orig_node]
                    symmetric_replacements.append(new_node)
                else:
                    new_node_dist_dict[orig_node][new_node] = default
                    default_replacements.append(new_node)
            if len(symmetric_replacements) > 0 or len(default_replacements) > 0:
                msg = 'Original node ({}) missing distances'.format(orig_node)
                if len(symmetric_replacements) > 0:
                    msg = '\n\t'.join([msg,
                                       'distances to new nodes ({}) replaced with symmetric distance'
                                       .format(', '.join([str(i) for i in symmetric_replacements]))])
                if len(default_replacements) > 0:
                    msg = '\n\t'.join([msg,
                                       'distances to new nodes ({}) replaced with default ({}) distance'
                                       .format(', '.join([str(i) for i in default_replacements]),
                                               default)])
                    
                missing_distances[new_node] = msg
        
        # Print warning message if necessary
        if len(missing_distances) > 0:
            warnings.warn('\n\n'.join([value for value in missing_distances.values()]))
            
        return(new_node_dist_dict)
        
    def _get_updated_node_dist_dict_comprehension(self,new_nodes,orig_nodes,node_dist_dict,default=0):
        '''
        Takes the provided node_dist_dict and makes sure new nodes have to and from distances
        
        For the new nodes, it makes sure they have from and to distances, using
        the symmetric value if present or the default. Then loops through the original
        nodes from the object and makes sure there are distances to all the new nodes.
        Keeps all provided distances between original nodes and doesn't update the
        non-provided symmetric part. This function is pythonic in using comprehension
        but does not provide user warnings of missing distances.

        Parameters
        ----------
        new_nodes : set
            Nodes being added to the TSP from this step.
        orig_nodes : set
            Nodes that were already in the TSP.
        node_dist_dict : dict of dicts
            Outer keys are new and original nodes. Inner keys are other nodes besides this outer node.
            Inner values are the distances
        default : numeric, optional
            The value to use when a required distance doesn't exist and the
            symmetric value doesn't exist. The default is 0.

        Returns
        -------
        new_node_dist_dict : dict of dicts
            The updated node_dist_dict with all required distances between new
            nodes and existing nodes.

        '''
        new_node_dist_dict = {
                # entries for new nodes
                # make a dict for each new node that has distances to other nodes (existing and new nodes)
                # that distance is either the entry in provided dict, the inverse entry
                # or the default distance
                **{new_node:{other_node:node_dist_dict[new_node].get(other_node,
                                                                     node_dist_dict.get(other_node,
                                                                                        {new_node:default}).get(new_node,default))
                             for other_node in new_nodes.union(orig_nodes).difference(set([new_node]))}
                   for new_node in new_nodes},
                
                # entries for existing nodes
                # need to add a distance to every new node provided (first dict)
                # plus keep any updated distances provided in the dict (second dict)
                **{orig_node:{
                    # get the provided distance from the orig_node to each new_node
                    # if not provided, get the provided distance from the new_node to the orig_node (symmetric),
                    # and if that's not provided, use the default
                    **{new_node:node_dist_dict.get(orig_node,
                                                   {new_node:node_dist_dict[new_node].get(orig_node,default)}).get(new_node,default)
                       for new_node in new_nodes},
                    # get the provided distances fom orig_node to other original nodes
                    # if they exist in the provided node_dist_dict
                    **{other_orig_node:node_dist_dict.get(orig_node,
                                                          {other_orig_node:default}).get(other_orig_node,default)
                       for other_orig_node in node_dist_dict.get(orig_node,{}).keys()}}
                    for orig_node in orig_nodes}
                }
        return(new_node_dist_dict)
        
        
    def add_nodes(self,node_dist_dict : dict,default = 0):
        '''
        Add nodes or update distances in the TSP object
        
        Must provide the dict of dicts to maintain the complete graph representation.
        If adding nodes without providing distances 

        Parameters
        ----------
        node_dist_dict : dict of dicts
            Outer keys are nodes to add/update. Inner keys are the endpoint of the edge to update.
            If you want to update all required distances with a default value,
            the inner dictionaries can be empty dictionaries. If the edges are
            symmetric (distance from A to B is equal to distance from B to A)
            when adding a new node then you can just provide one of those distances
            and it will be used for either. If you're updating edges however,
            you must provide both directions.
        default : numeric
            The default value to use if a required edge distance not included.
            The default is 0
        

        Returns
        -------
        None.

        '''
        
        new_nodes = set(node_dist_dict.keys()).difference(self.nodes)
        orig_nodes = self.nodes
        
        
        # If there are new nodes we need to add along with their distances
        # Make sure the distances from and to the new nodes are entries in the dict
        # If the to distances don't exist, use the from distances (if exist)
        # and as a last resort, use the default value
        if len(new_nodes) > 0:
            
            node_dist_dict = self._get_updated_node_dist_dict_for(new_nodes,
                                                             orig_nodes,
                                                             node_dist_dict,default=default)
            # This function is more pythonic (list comprehensions), but doesn't provide the warnings
            # node_dist_dict = self._get_updated_node_dist_dict_comprehension(new_nodes,
            #                                                           orig_nodes,
            #                                                           node_dist_dict,default=default)
            
            
            # Add the new nodes to the node set
            self.nodes.update(new_nodes)

        # Actually update the distance dict of dicts
        self._update_dist_dod(node_dist_dict,default=default)
        
        
        
        
    def _update_dist_dod(self,node_dist_dict : dict,default=0):
        '''
        Updates values in the dist_dod with values in the node_dist_dict
        
        Only updates existing entries and expects all keys in the outer and inner dict
        to already exist in the TSP

        Parameters
        ----------
        node_dist_dict : dict
            Dict of dicts where outer key are the "from" nodes. The inner dicts
            are keyed by the "to" nodes and have the from-to distance as the values

        Returns
        -------
        None.

        '''
        for node in node_dist_dict.keys():
            self.dist_dod[node] = {other_node:node_dist_dict[node].get(other_node,
                                                                       self.dist_dod.get(node,
                                                                                         {other_node:'never_used_but_created'}).get(other_node,default))
                                         for other_node in self.nodes.difference(set([node]))}
    
    
    def make_tour(self,funct = 'random',**kwargs):
        
        default_dict = {'random':self.random_tour_list,
                        'ordered':self.ordered_tour_list,
                        'greedy':self.greedy_tour_list}
        default_str = 'random'
        
        if type(funct) == str:
            if funct not in default_dict.keys():
                warnings.warn('{} is not a valid string function type. It must be one of ({}). Defaulting to {}'.format(funct,
                                                                                                                      ', '.join(default_dict.keys()),
                                                                                                                      default_str))
                funct = default_str
            funct = default_dict[default_str]
            
        tour = TSPTour.from_tsp(self,funct,**kwargs)
        return(tour)
    
    def random_tour_list(self):
        '''
        Make a random tour (permutation) of the nodes in the TSP
        
        Returns
        -------
        tour_list : list
            The list of node visits in this tour; doesn't loop back to starting node.
        '''

        tour = random.sample(self.nodes,len(self.nodes))
        return(tour)
    
    
    def ordered_tour_list(self,order=None):
        '''
        Return a list of the nodes in the TSP as they are.
        
        Simply converts self.nodes into a list

        Returns
        -------
        tour_list : list
            The list of node visits in this tour; doesn't loop back to starting node.
        '''
        
        tour_list = list(self.nodes)
        return(tour_list)
    
    def greedy_tour_list(self,start_node=None):
        '''
        Return a tour starting at start_node that uses the best possible edge
        
        From the starting node, find the closest node and continue to add the closest
        node successively. If, not provided (or a valid node in the TSP), start_node defaults to a random node
        
        Parameters
        ----------
        random_node : node in self.nodes
            The node to begin the greedy search from.

        Returns
        -------
        tour_list : list
            The list of node visits in this tour; doesn't loop back to starting node.
        '''
        
        if start_node not in self.nodes:
            start_node = random.choice(self.nodes)
            
        tour_list = list(start_node)
            
        non_visited_nodes = self.nodes.remove(start_node)
        
        # recursively add the next best node from the current node
        while len(non_visited_nodes) > 0:
            best_dist = None
            best_node = None
            poss_edge_dict = self.dist_dod[tour[-1]]
            
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
            
        
class TSPTour(object):
    
    def __init__(self,tsp,tour_list):
        self.tour_list = tour_list
        self.dist_dod = tsp.dist_dod
        self.distance = self.get_distance()
        
    def __iter__(self):
        '''
        Iterates through the nodes in the tour_list
        '''
        for node in self.tour_list:
            yield(node)
            
    def __str__(self):
        return('The tour is ({}). \nThe distance is: {}.'.format(', '.join[self.tour_list],
                                                                 self.distance))
        
    def get_distance(self):
        return(sum([self.dist_dod[self.tour_list[i]][self.tour_list[i+1]]
                    for i in range(len(self.tour_list)-1)]
                   # distance from last node back to the start
                   + [self.dist_dod[self.tour_list[-1]][self.tour_list[0]]]))
    
    def two_swap(self):
        nodes_to_swap = random.sample(range(len(self.tour_list)),2)
        
        # new_dist = self.distance
        
        # ind_dist = abs(nodes_to_swap[0] - nodes_to_swap[1])
        
        # for ind in nodes_to_swap:
        #     if ind == 0:
        #         new_dist -= self.dist_dod[ind][]
        #     elif ind == len(self.tour_list) - 1:
                
        #     else:
                
        # swap the nodes
        self.tour_list[nodes_to_swap[0]], self.tour_list[nodes_to_swap[1]] = self.tour_list[nodes_to_swap[1]], self.tour_list[nodes_to_swap[0]]
        
        self.distance = self.get_distance()
        
    @classmethod
    def from_tsp(cls,tsp,funct,**kwargs):
        return(cls(tsp,funct(tsp,**kwargs)))

       
#%%
# bar = TSP({1:{2:13},2:{1:13}})
# bar.add_nodes({3:{}},default=47)
# bar.add_nodes({4:{1:1,2:2,3:3},
#                1:{2:50,4:-1},
#                2:{4:99}})
    