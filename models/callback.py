'''
Contains a component checking based subtour elimination algorithm
'''

from gurobipy import Model, GRB, quicksum
import networkx as nx

def component_subtourelim(model, where):
    '''
    Find the components of the graph
    Select the smallest components (number of vertices)
    Force the model to have at least one edge connecting the
        component to its complement
    '''
    if where == GRB.Callback.MIPSOL:
        G = nx.Graph()
        edges = [
            edge.vertices
            for edge in model._edges
            if model.cbGetSolution(model._edgevar[edge.vertices])]
        G.add_edges_from(edges)

        components = sorted(nx.connected_components(G), key=len)

        if len(components) != 1:
            component = components[0]
            lhs = quicksum(
                model._edgevar[edge.vertices]
                for vertex1 in component
                for vertex2, edge in vertex1.incident.iteritems()
                if vertex2 not in component)
            rhs = 1
            model.cbLazy(lhs >= rhs)

def cycle_subtourelim(model, where):
    '''
    Find the components of the graph
    Select the smallest components (number of vertices)
    Force the model to have at least one edge connecting the
        component to its complement
    '''
    if where == GRB.Callback.MIPSOL:
        G = nx.Graph()
        edges = [
            edge.vertices
            for edge in model._edges
            if model.cbGetSolution(model._edgevar[edge.vertices])]
        G.add_edges_from(edges)

        cycle = nx.find_cycle(G) 
        lhs = quicksum(
            model._edgevar[vertex1.incident[vertex2].vertices]
            for vertex1, vertex2 in cycle
        )
        rhs = len(cycle) - 1
        model.cbLazy(lhs <= rhs)
