'''
Create a lower bound for the problem as the MST heuristic
is a 2 approximation
'''
from time import time

from mst import mst_heuristic
from io import writer

def halfmst_heuristic(n, tofile=False):
    '''
    :n: the network object
    '''
    start = time()
    algorithm_name = 'halfmst_heuristic'
    temp_consumption, temp_objective = mst_heuristic(n, tofile=False)

    consumption = {
        vertex: weight/2 for vertex, weight in temp_consumption.iteritems()}
    objective = temp_objective/2

    duration = time() - start

    if tofile:
        writer(n, consumption, objective, duration, algorithm_name)

    return consumption, objective
