'''
Vertex object
'''

class Vertex(object):
    '''
    :id: vertex id
    '''
    def __init__(self, id):
        self.id = id
        self.coord = []
        self.distance = {}
        self.incremental = {}
        self.neighbours = []
