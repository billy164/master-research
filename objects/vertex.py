'''
Vertex object
'''
from collections import OrderedDict


class Vertex(object):
    '''
    :name: vertex name
    '''
    def __init__(self, name):
        self.name = name
        self.coord = []
        self.distance = {}
        self.incremental = OrderedDict()
        self.neighbours = []
