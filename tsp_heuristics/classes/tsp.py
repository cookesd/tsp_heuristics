# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 12:12:13 2020

@author: dakar
"""



import warnings
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
        
        
    def add_nodes(self,node_dist_dict):
        pass
    
    

       

    