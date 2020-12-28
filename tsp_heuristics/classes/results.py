# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 14:02:28 2020

@author: dakar
"""

import matplotlib.pyplot as plt

class SimAnnealRes(object):
    
    def __init__(self,sol_list,best_it,best_sol):
        self.sol_list = sol_list
        self.best_it = best_it
        self.best_sol = best_sol
        self._dist_list = [sol.distance for sol in self.sol_list]
        
    @property
    def dist_list(self):
        return(self._dist_list)
    
    @dist_list.getter
    def dist_list(self):
        return(self._dist_list)
    
    # should implement sol_list as a property
    # then update best_it, best_sol, and dist_list whenever it updates
        
        
    def __str__(self):
        return('After {} iterations, the best solution was found at iteration {} and has distance of {}.'.format(len(self.sol_list),
                                                                                                                     self.best_it,
                                                                                                                     self.best_sol.distance))
        
    def __len__(self):
        return(len(self.sol_list))
    
    def __lt__(self,res2):
        return(self.best_sol < res2.best_sol)
    def __gt__(self,res2):
        return(self.best_sol > res2.best_sol)
    def __le__(self,res2):
        return(self.best_sol <= res2.best_sol)
    def __ge__(self,res2):
        return(self.best_sol >= res2.best_sol)
    def __eq__(self,res2):
        return(self.best_sol == res2.best_sol)
    def __ne__(self,res2):
        return(self.best_sol != res2.best_sol)
    
    def plot(self,**kwargs):
        plt.plot(list(range(len(self.sol_list))),self.dist_list,'bo-',**kwargs)
        plt.plot(self.best_it,self.best_sol.distance,'r^')
        plt.title('{} Iterations \nBest distance: {:.2f}'.format(len(self) - 1,float(self.best_sol.distance)))