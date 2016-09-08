'''
Contains the following exceptions:
    - NotCompleteGraph
    - ConsumptionNotFound
'''

class NotCompleteGraph(Exception):
    '''
    This checks if the graph contains n choose 2 edges
    '''
    pass

class ConsumptionNotFound(Exception):
    '''
    If we can't warm start a vertex for a given consumption value
    '''
    pass
