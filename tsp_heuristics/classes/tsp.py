# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 12:12:13 2020

@author: dakar
"""



import warnings

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
        
        
    def add_nodes(self,node_dist_dict):
        pass
    
def make_tsp(incoming_data,obj_to_use=TSP()):
    
    # dict of dicts
    if isinstance(incoming_data,dict):
        tsp_from_dod = obj_to_use
        tsp_from_dod.dist_dod = incoming_data
        tsp_from_dod.nodes.update(tsp_from_dod.dist_dod.keys())
        return(tsp_from_dod)
    
    # list/tuple of lists/tuples [(source, taget, distance)
    # for source, target in graph node combinations of size two (source != target)]
    elif isinstance(incoming_data,(list,tuple)):
        tsp_from_list_tup = obj_to_use
        for s, t, dist in incoming_data:
            if s not in tsp_from_list_tup.dist_dod.keys():
                tsp_from_list_tup.dist_dod[s] = {}
            tsp_from_list_tup.dist_dod[s].update({t:dist})
            tsp_from_list_tup.nodes.update((s,t))
        return(tsp_from_list_tup)
    
    # pandas df
    try:
        import pandas as pd
        if isinstance(incoming_data,pd.DataFrame):
            tsp_from_df = obj_to_use
            cols = list(incoming_data.columns)
            source_col = 'source'
            target_col = 'target'
            dist_col = 'distance'
            
            
            if incoming_data.shape[0] == incoming_data.shape[1]:
                # adjacency matrix
                
                tsp_from_df.nodes.update(cols)
                # iterate through rows making the row series a dict and removing
                # what would be the diagonal entry
                tsp_from_df.dist_dod = {cols[i]:{key:val
                                                 for key,val in row[1].to_dict().items()
                                                 if key != cols[i]}
                                        for i,row in enumerate(incoming_data.iterrows())}
                
                
            elif all([col in cols for col in [source_col,target_col,dist_col]]):
                # edgelist
                tsp_from_df.nodes.update(set([*list(incoming_data[source_col].unique),
                                              *list(incoming_data[target_col].unique)]))
                tsp_from_df.dist_dod = {node:{} for node in tsp_from_df.nodes}
                for index,row in incoming_data.iterrows():
                    tsp_from_df.dist_dod[row[1][source_col]].update({row[1][target_col]:row[1][dist_col]})
            else:
                print('''Wrong format of pandas dataframe. It must have equal dimensions
                      or contain columns ({})'''.format(', '.join([source_col,target_col,dist_col])))
            return(tsp_from_df)
        
    except ImportError:
        msg = 'pandas not found.'
        warnings.warn(msg, ImportWarning)
        
    