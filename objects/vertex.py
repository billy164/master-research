'''
Vertex object
'''
from collections import OrderedDict


class Vertex(object):
    '''
    :name: vertex name
    coord -> [xpos, ypos]
    distance -> {vertex: d_{ij}^alpha}
    incremental -> {vertex: incremental cost}
    incident -> {vertex: edge}
    '''
    def __init__(self, name):
        self.name = name
        self.coord = []
        self.distance = {}
        self.incremental = OrderedDict()
        self.incident = {}
