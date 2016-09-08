'''
The MST heuristic described by Kirousis et al
'''
from collections import defaultdict
from time import time
import networkx as nx

from io import writer
from exceptions import NotCompleteGraph
from utils import nchoose2

def mst_heuristic(n, tofile=False):
    '''
    :n: the network object
    '''
    if nchoose2(n.numvertices) != len(n.edges):
        raise NotCompleteGraph('The graph has been preprocessed.')

    else:
        start = time()
        algorithm_name = 'mst_heuristic'
        consumption = defaultdict(float)
        objective = 0

        graph = nx.Graph()
        weighted_edges = [edge.vertexweighttuple for edge in n.edges]
        graph.add_weighted_edges_from(weighted_edges)
        tree = nx.minimum_spanning_tree(graph)

        for vertex1, vertex2, weight in tree.edges(data=True):
            consumption[vertex1] = max(consumption[vertex1], weight['weight'])
            consumption[vertex2] = max(consumption[vertex2], weight['weight'])
        objective = sum(consumption[vertex] for vertex in n.vertices)

        duration = time() - start

        if tofile:
            writer(n, consumption, objective, duration, algorithm_name)

        return consumption, objective
