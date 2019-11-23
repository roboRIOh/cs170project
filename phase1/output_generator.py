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
        row = [h for h in content[i].split()]
        for i in range(len(row)):
            if row[i] == 'x':
                row[i] = 0
            elif row[i] == '1':
                row[i] = 1
        adj_mat.append(row)

    graph = su.adjacency_matrix_to_graph(adj_mat)[0]
    nx.draw(graph)
    plt.savefig("filename.png")

    return graph

def shortest_paths(G):
    paths = nx.shortest_path(G, 1, 20)
    print(paths)

G = create_graph('50.in')
shortest_paths(G)
