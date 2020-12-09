#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
from gurobipy import *

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    g = nx.Graph()
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        g.add_node(int(parts[0]))
        g.add_edge(int(parts[0]), int(parts[1]))

    # build a trivial solution
    # every node has its own color
    cliques = nx.find_cliques(g)
    cliques_dict = {}
    for i in range(node_count):
        cliques_dict[i] = []
    for clique in cliques:      
        cliques_dict[len(clique)].append(clique)
    m = Model()
    x = {}
    y = {}
    for i in range(node_count): 
        for k in range(node_count):
    	    x[(i,k)] = m.addVar(vtype=GRB.BINARY, name="x%d%d" % (i,k)) 
    for k in range(node_count):
        y[k] = m.addVar(vtype=GRB.BINARY, name="y%d" % k) 	
    m.update()
    # Add constraints
    for i in range(node_count): 
    	m.addConstr(quicksum(x[(i,k)] for k in range(node_count)) == 1)
    for k in range(node_count):
        for i, j in edges:
            m.addConstr(x[(i,k)] + x[(j,k)] <= y[k])
    for size in cliques_dict:
        for l in cliques_dict[size]:
            for c in l:
                aux = 0
                for n in range(size):
                    aux += n
                m.addConstr(quicksum(k*x[(c,k)] for k in range(node_count)) >= aux)       
    m.setObjective(quicksum(y[k] for k in range(node_count)), GRB.MINIMIZE) 
    m.optimize()
    count_used = sum(int(y[k].X) for k in range(node_count))
    solution = []
    for i in range(node_count): 
        for k in range(node_count):
    	    if x[(i,k)].X == 1:
                solution.append(k)
    # prepare the solution in the specified output format
    output_data = str(count_used) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

