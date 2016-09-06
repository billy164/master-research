'''
File contains:
    - writer
'''
import json
import os

def writer(n, consumption, objective, time, algorithm_name):
    '''
    :n: Network object
    :consumption: a dictionary containing vertex objects -> power consumption
    :objective: cost of a solution
    :time: how long it took to run the algorithm
    :algorithm_name: name of the algorithm
    '''
    data = {}
    data['consumption'] = {
        vertex.name: weight for vertex, weight in consumption.iteritems()
    }
    data['objective'] = objective
    data['time'] = time
    data['algorithm_name'] = algorithm_name

    dirs = os.path.join('results', n.numvertices, algorithm_name)
    fullpath = os.path.join(dirs, n.seed)

    if not os.path.exists(dirs):
        os.makedirs(dirs)

    with open(fullpath, 'w') as outfile:
        json.dump(data, outfile)
