'''
The althaus model

http://s3.amazonaws.com/academia.edu.documents/39774928/Power_efficient_range_assignment_in_ad-h20151107-15204-wewd28.pdf?AWSAccessKeyId=AKIAJ56TQJRTWSMTNPEA&Expires=1473241752&Signature=11dNrYeby6SwmRi1NZ/xl4HhDto=&response-content-disposition=inline;%20filename=Power_efficient_range_assignment_in_ad-h.pdf

:EPS: is a tolerance value in warm starting
'''

from gurobipy import Model, GRB, quicksum
from custom_exceptions import ConsumptionNotFound
from callback import subtourelim
from io import writer

EPS = 0.001

class Althaus(object):
    '''
    :n: Network object
    :params: a dictionary containing variables to control the model
    :warmstartsolution: a dictionary going from vertices to its
        consumption
    '''
    def __init__(self, n, params, warmstartsolution={}):
        self.n = n
        self.params = params
        self.warmstartsolution = warmstartsolution
        self.edgevar = {}
        self.arcvar = {}

        self.create_model()

    def create_model(self):
        '''
        Compiles everything into the model
        '''
        self.m = Model()
        self._variables()
        self.m.update()
        self._objective()
        self._constraints()
        self._set_model_parameters()

        if self.params['warmstart'] and self.warmstartsolution:
            self._warmstart()

        if self.params['validinequality']:
            self._valid_inequalities()

        self.m.update()

    def optimise(self):
        '''
        The subtour elimination callback will be used if
        params['callback'] == True
        Otherwise, it will create a lower bound on the optimal
        solution
        '''
        if self.params['callback']:
            self._includeobjects()
            self.m.params.LazyConstraints = 1
            self.m.optimize(subtourelim)
        else:
            self.m.optimize()

    def output(self, tofile=False):
        '''
        like the heuristics, it returns:
            - consumption
            - time
            - objective
        '''
        n = self.n
        consumption = {
            vertex1: edge.weight
            for vertex1 in self.n.vertices
            for vertex2, edge in vertex1.incident.iteritems()
            if self.edgevar[edge.vertices].x > 0.5
        }
        objective = self.m.objVal
        duration = self.m.Runtime

        if tofile:
            algorithm_name = 'althaus' if self.params['callback'] else 'althaus_lb'
            writer(n, consumption, objective, duration, algorithm_name)

        #return consumption, objective
        consumption = {vertex.name: edgeweight for vertex, edgeweight in consumption.iteritems()}
        return consumption, objective

    def _variables(self):
        '''
        creates the edge(x) and arc(y) variables
        '''
        self._variables1()
        self._variables2()

    def _objective(self):
        '''
        sum over all arcs:
        d_{ij}^alpha * y_{ij}
        '''
        objective = quicksum(
            edge.weight*self.arcvar[vertex1, vertex2]
            for vertex1 in self.n.vertices
            for vertex2, edge in vertex1.incident.iteritems())

        self.m.setObjective(objective, GRB.MINIMIZE)

    def _constraints(self):
        '''
        Generates all the constraints
        '''
        self._constraint1()
        self._constraint2()
        self._constraint3()
        self._constraint4()

    def _valid_inequalities(self):
        '''
        There are none for the Althaus model
        '''
        pass

    def _warmstart(self):
        '''
        set
        '''
        for vertex1 in self.n.vertices:
            for vertex2, distance in vertex1.distance.iteritems():
                if abs(distance - self.warmstartsolution[vertex1]) <= EPS:
                    try:
                        self.edgevar[vertex1, vertex2].start = 1
                    except KeyError:
                        self.edgevar[vertex2, vertex1].start = 1
                    break
            else:
                raise ConsumptionNotFound(
                    'Vertex {} does\'t have a distance {}'.format(
                        vertex1.name, self.warmstartsolution[vertex1]))

    def _set_model_parameters(self):
        '''
        Change the following parameters in the Gurobi model
        - Threads
        '''
        if 'Threads' in self.params:
            self.m.Params.Threads = self.params['Threads']

    def _variables1(self):
        '''
        creates the x variables.
        Each x variable corresponds to an unique edge
        '''
        self.edgevar = {
            edge.vertices: self.m.addVar(vtype=GRB.BINARY)
            for edge in self.n.edges}

    def _variables2(self):
        '''
        Creates the y variables.
        An arc is created by assigning a direction on an edge.
        Each y variable corresponds to an unique arc.
        '''
        self.arcvar = {
            (vertex1, vertex2): self.m.addVar(vtype=GRB.BINARY)
            for vertex1 in self.n.vertices
            for vertex2 in vertex1.incident.keys()}

    def _constraint1(self):
        '''
        Each vertex has one arc that determines its range
        '''
        for vertex1 in self.n.vertices:
            lhs = quicksum(
                self.arcvar[vertex1, vertex2]
                for vertex2 in vertex1.incident.keys())
            rhs = 1
            self.m.addConstr(lhs >= rhs)

    def _constraint2(self):
        '''
        If an edge (v1, v2) is in the solution, then there exists
        at least arc leaving from v1 with a weight equal or greater
        than the edge

        Let g_vertex be a vertex where its edge weight is greater
        than the original edge
        '''
        for edge in self.n.edges:
            vertex1, vertex2 = edge.vertices
            lhs = self.edgevar[vertex1, vertex2]
            rhs = quicksum(
                self.arcvar[vertex1, g_vertex]
                for g_vertex, g_weight in vertex1.distance.iteritems()
                if g_weight >= edge.weight)
            self.m.addConstr(lhs <= rhs)

    def _constraint3(self):
        '''
        Very similar to constraint 2.
        This time it is acting on vertex2
        '''
        for edge in self.n.edges:
            vertex1, vertex2 = edge.vertices
            lhs = self.edgevar[vertex1, vertex2]
            rhs = quicksum(
                self.arcvar[vertex2, g_vertex]
                for g_vertex, g_weight in vertex2.distance.iteritems()
                if g_weight >= edge.weight)
            self.m.addConstr(lhs <= rhs)

    def _constraint4(self):
        '''
        Need numvertices - 1 edges in the solution
        '''
        lhs = quicksum(
            self.edgevar[edge.vertices]
            for edge in self.n.edges)
        rhs = self.n.numvertices - 1
        self.m.addConstr(lhs <= rhs)
        self.m.addConstr(lhs >= rhs)

    def _includeobjects(self):
        '''
        Add the edges, vertices and edge variables to
        the Gurobi model
        '''
        self.m._edges = self.n.edges
        self.m._vertices = self.n.vertices
        self.m._edgevar = self.edgevar
