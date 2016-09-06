'''
A network object for the graph
'''
from itertools import combinations
from math import sqrt
import random

from vertex import Vertex
from edge import Edge

class Network(object):
    '''
    creates a graph by (V, E)
    '''
    def __init__(self, numvertices, alpha, seed=0, max_coord=100):
        '''
        :seed: random seed
        :alpha: power attenuation (d_{ij}^\alpha)
        :max_coord: maximum value for coordinate [0, maxcoord)
        '''
        self.numvertices = numvertices
        self.alpha = alpha
        self.seed = seed
        self.max_coord = max_coord
        self.vertices = []
        self.edges = []

        self.generateinstance()
        self.addinformation()

    def generateinstance(self):
        '''
        generate the network with vertices and edges
        Add in the positions of vertices
        '''
        self._generatevertices()
        self._generateedges()
        self._generatepositions()

    def addinformation(self):
        '''
        information on the network such as edge weights, neighbours and incremental weights
        '''
        self._addweight()
        self._addneighbours()
        self._addincremental()

    def preprocess(self, edges):
        '''
        replace self.edges with edgelist
        add in the necessary information on the new network
        '''
        self.edges = edges
        self.addinformation()

    def _generatevertices(self):
        '''
        Creates a list of Vertex
        '''
        self.vertices = [Vertex(name) for name in range(self.numvertices)]

    def _generateedges(self):
        '''
        Creates a list of edges based on Vertex
        '''
        self.edges = [
            Edge(vertex1, vertex2)
            for vertex1, vertex2 in combinations(self.vertices, 2)
        ]

    def _generatepositions(self):
        '''
        Add position information for the vertices
        '''
        random.seed(self.seed)
        for vertex in self.vertices:
            xpos = self.max_coord*random.random()
            ypos = self.max_coord*random.random()
            vertex.coord = [xpos, ypos]

    def _addweight(self):
        '''
        Find the weight between two vertices
        '''
        for edge in self.edges:
            vertex1, vertex2 = edge.vertices
            edge_weight = self._power(vertex1, vertex2)
            vertex1.distance[vertex2] = edge_weight
            vertex2.distance[vertex1] = edge_weight
            edge.weight = edge_weight

    def _addneighbours(self):
        '''
        Find all the neighbours of a vertex
        '''
        for edge in self.edges:
            vertex1, vertex2 = edge.vertices
            vertex1.neighbours.append(vertex2)
            vertex2.neighbours.append(vertex1)

    def _addincremental(self):
        '''
        Use edge weights and neighbours to find the incremental edge costs
        - sort the neighbours of a vertex with respect to its neighbours
        - ancestor_cost is the power required to reach the next closest vertex
            (initialise it with 0)
        - incremental cost is (power - ancestor_cost)
        '''
        for vertex in self.vertices:
            ancestor_cost = 0
            sorted_list = sorted(vertex.distance.items(), key=lambda x: x[1])
            for ancestor, power in sorted_list:
                vertex.incremental[ancestor] = power - ancestor_cost
                ancestor_cost = power

    def _power(self, vertex1, vertex2):
        '''
        calculates the power required to connect to nodes
        d_{ij}^\alpha
        '''
        return sqrt(
            (vertex1.coord[0] - vertex2.coord[0])**2 +
            (vertex1.coord[1] - vertex2.coord[1])**2
            )**self.alpha
