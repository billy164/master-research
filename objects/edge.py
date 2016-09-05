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
