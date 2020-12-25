# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 14:59:32 2020

@author: dakar
"""


def make_tsp(incoming_data,obj_to_use,index_col=None):
    '''
    Read the data from multiple possible data types
    
    Attempts to read data from different data types and adds it to the
    provided object (default is a TSP object). Possible data types are:
    dict of dicts ({source:{target:distance for target in source's neighbors} for source in nodes}),
    list/tuple of list/tuples (the inner lists/tuples must have form (source, target, distance)),
    pandas.DataFrame adjacency matrix with distances
    pandas.DataFrame edgelist (columns must be ['source','target','distance'])
    path to csv file containing either of the pandas entry types
    
    Heavily adapted from networkx graph classes and convert modules

    Parameters
    ----------
    incoming_data : dict of dicts, list/tuple of lists/tuples, adjacency matrix/edgelist in pd.DataFrame, path to csv file
        Data to add to the provided object.
    obj_to_use : object TSP
        The object to add the data to.
    index_col : int (zero indexed)
        The column index that contains the index. None if not provided

    Returns
    -------
    Object with data added.

    '''
    
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
            

            # pandas adjacency matrix            
            if incoming_data.shape[0] == incoming_data.shape[1]:
                
                tsp_from_df.nodes.update(cols)
                # iterate through rows making the row series a dict and removing
                # what would be the diagonal entry
                tsp_from_df.dist_dod = {cols[i]:{key:val
                                                 for key,val in row[1].to_dict().items()
                                                 if key != cols[i]}
                                        for i,row in enumerate(incoming_data.iterrows())}
                
            # pandas edgelist
            elif all([col in cols for col in [source_col,target_col,dist_col]]):
                tsp_from_df.nodes.update(set([*list(incoming_data[source_col].unique),
                                              *list(incoming_data[target_col].unique)]))
                tsp_from_df.dist_dod = {node:{} for node in tsp_from_df.nodes}
                for index,row in incoming_data.iterrows():
                    tsp_from_df.dist_dod[row[1][source_col]].update({row[1][target_col]:row[1][dist_col]})
            else:
                print('''Wrong format of pandas dataframe. It must have equal dimensions
                      or contain columns ({})'''.format(', '.join([source_col,target_col,dist_col])))
            return(tsp_from_df)
        
        # path to csv file
        else:
            if isinstance(incoming_data,str):
                dat_df = pd.read_csv(incoming_data,index_col = index_col)
                return(make_tsp(incoming_data=dat_df,obj_to_use=obj_to_use))
        
    except ImportError:
        msg = 'pandas not found.'
        warnings.warn(msg, ImportWarning)
        
    # Default return
    warnings.warn('Provided data is not of accepted format')
    return(obj_to_use)