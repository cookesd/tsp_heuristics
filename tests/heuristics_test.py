# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 14:10:22 2020

@author: dakar
"""

import tsp_heuristics as th

# make tsp problem by reading data
data_file = './tests/nfl_city_data/NFLdata.csv'

nfl_tsp = th.TSP(data_file,index_col=0)


starting_tour = th.TSPTour.from_tsp(nfl_tsp,'random')

final_sol = th.simulated_annealing(starting_tour,'n_swap',n=3,num_iter=10000)

print(final_sol)

my_plot = final_sol.plot()
