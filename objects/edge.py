'''
Non directed edge object
'''

class Edge(object):
    '''
    Takes two vertices
    '''
    def __init__(self, vertex1, vertex2):
        self.vertices = [vertex1, vertex2]
        self.weight = 0

    @property
    def edgetuple(self):
        '''
        returns the tuple (vertex1, vertex2, weight)
        '''
        return self.vertices[0], self.vertices[1], self.weight
