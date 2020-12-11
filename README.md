# tsp_huerustics

This package intends to implement heuristics for the Travelling Salesman Problem on a complete graph. The interface is to create a TSP object which has a solve method with parameters for the `heuristic` to use and the `**kwargs` for heuristic parameters. It returns a TSP solution object which contains as attributes the best solution from the heuristic and the historic list of solutions. The TSP solution object has methods to visualize the historical and best solutions.


## Proposed Heuristics

- Simulated Annealing
- Genetic Algorithms

## Proposed Visualizations

- Animation of historic TSP tours (networkx/matplotlib)
- Line graph of historical tour lengths with best tour annotated (plotnine)
- `networkx` drawing of best tour