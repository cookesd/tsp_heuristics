# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:00:25 2020

@author: dakar
"""

def simulated_annealing(starting_sol,generation_funct,num_iter,starting_temp=100,cooling_const=.995,**kwargs):
    '''
    Implements simulated annealing heuristic and returns best found solution
    
    Generates new solutions and accepts/rejects based on solution objective or
    randomly based on iteration number/annealing parameters (starting_temp, cooling_const).
    If a new solution is worse than the initial, then we accept it with probablility
    1 - e^{-(t*((new_cost - current_cost)/current_cost)*c)}    

    Parameters
    ----------
    starting_sol : solution object (TSPTour)
        The initial solution to start generating additional solutions.
        Must have attribute `distance` representing the cost of the solution.
    generation_funct : str or function
        The function to use to generate new solutions. If class function, pass name as string.
        Can use **kwargs to pass additional arguments
    num_iter : int
        The max number of iterations to build new solutions.
    starting_temp : numeric, optional
        Affects the magnitude of exponential distribution. The default is 100.
    cooling_const : numeric, optional
        Affects how likely we are to accept worse solutions. The default is .995.

    Returns
    -------
    best_sol : type(starting_sol).

    '''
    
    
    
    # store current solution and best solution
    
    # iterate for num_iter
    
    # make temp solution (deepcopy of curr solution)
        # check if generation_funct is string or functional
            # if string, use the class method to generate temp solution
    
    # check if better than current solution
    
        # if so, check if solution better than best solution
            # if so, then keep track of it
    
    # if not, check if probability better than annealing acceptance prob
    
    # return best solution
    pass

def tabu_search(obj,generation_funct,num_iter,tabu_len):
    pass

# def genetic_alg(obj,)