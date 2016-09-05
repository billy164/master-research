# master-research
An re-implemented version of my masters research project: Preprocessing for the min power range assignment problem.

---
## Problem description
Given a graph _G_ = (_V, E_), find a spanning tree such that:

* alpha is a constant; representing the environmental factor.
* The edge weights are given by the euclidean distance raised to the power of alpha.
* Each vertex consumes power equal to the largest incident edge in the spanning tree.
* The cost of a network is given by total power consumption over all vertices.

---
## Preprocessing
We start with a complete graph for _G_ and reduce the size of the edge set to produce _G*_. The optimal solution in _G_ and _G*_ must have the same objective value.

To do this, we explore:

* Heuristics to find upper and lower bounds. 
* Integer programs to find the optimal solution.
