# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:00:25 2020

@author: dakar
"""

import copy
import math
import random

def simulated_annealing(starting_sol,generation_funct,num_iter=1000,direction='min',starting_temp=100,cooling_const=.995,**kwargs):
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
        The max number of iterations to build new solutions. The default is 1000.
    direction : str {"min","max"}
        The direction of the optimization function. Whether you want to maximize or minimize.
        The default is "min".
    starting_temp : numeric, optional
        Affects the magnitude of exponential distribution. The default is 100.
    cooling_const : numeric, optional
        Affects how likely we are to accept worse solutions. The default is .995.

    Returns
    -------
    best_sol : type(starting_sol).

    '''
    
    compare_dict = {'min':'__lt__','max':'__gt__'}
    
    # store current solution and best solution
    current_sol = copy.deepcopy(starting_sol)
    best_sol = copy.deepcopy(starting_sol)
    # iterate for num_iter
    for it in range(num_iter):
        # make temp solution (deepcopy of curr solution)
        # check if generation_funct is string or functional
        # if string, use the instance method to generate temp solution
        if isinstance(generation_funct,str):
            temp_sol = getattr(current_sol,generation_funct,default=None)(**kwargs)
        else:
            temp_sol = generation_funct(current_sol,**kwargs)
            
        # check if better than current solution
        if getattr(current_sol,compare_dict.get(direction,'__lt__'))(temp_sol):
            current_sol = temp_sol
            # update the best solution if the temp sol is better
            if getattr(current_sol,compare_dict.get(direction,'__lt__'))(best_sol):
                best_sol = current_sol
        else:
            # if not, check if probability better than annealing acceptance prob
            # if temp_sol.distance close to current_sol.distance then probability higher
            # use abs in case we want to maximize (temp will be less than)
            acceptProb = math.exp(-(starting_temp*(abs(temp_sol.distance-current_sol.distance)
                                                   /current_sol.distance)*cooling_const))
            testProb = random.random()
            if testProb < acceptProb:
                current_sol = temp_sol
        
    # return best solution
    return(best_sol)
        
    
    
    
    
    
    
    
    

def tabu_search(obj,generation_funct,num_iter,tabu_len):
    pass

# def genetic_alg(obj,)