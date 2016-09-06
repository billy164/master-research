'''
Contains the following utils functions:
    - nchoose2
'''
from math import factorial

def nchoose2(numvertices):
    '''
    The number of edges in a complete graph of size numvertices
    '''
    return factorial(numvertices)/(2*factorial(numvertices-2))
