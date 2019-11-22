import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import student_utils as su

def create_graph(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    num_locations = int(content[0])
    num_homes = int(content[1])
    location_names = [int(l) for l in content[2].split()]
    home_names = [int(h) for h in content[3].split()]
    starting_point = int(content[4])

    adj_mat = []
    for i in range(5, len(content)):
        adj_mat.append([h for h in content[i].split()])

    graph_tup = su.adjacency_matrix_to_graph(adj_mat)[0]
    graph = graph_tup[0]

create_graph('50.in')
