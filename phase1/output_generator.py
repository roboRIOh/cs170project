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

    return graph, home_names, starting_point

def shortest_paths(G, start_node):
    paths = nx.shortest_path(G, start_node)
    return paths

def get_shortest_path(G, start_node, homes):
    origin = start_node
    path = [start_node]
    while homes != []:
        temp_paths = shortest_paths(G, start_node)
        for p in temp_paths:
            destination = temp_paths[p][-1]
            if (destination in homes):
                path.extend(temp_paths[p][1:])
                homes.remove(destination)
                start_node = destination
                break;
    path.append(origin)
    return path

def write_output_file(path, size):
    path_str_list = [str(p) for p in path]
    path_str = ' '.join(path_str_list)
    file = open(f'{size}.out',"w")
    file.write("{0}\n".format(path_str))
    print(path_str)
    file.write("{0}\n".format(len(path) - 2))
    print(len(path) - 2)
    for i in range(1, len(path) - 1):
        drop_off = str(path_str_list[i])
        file.write("{0} {0}\n".format(drop_off))
        print(drop_off)
    file.close()

for i in [50, 100, 200]:
    (G, homes, start_node) = create_graph(f'{i}.in')
    path = get_shortest_path(G, start_node, homes)
    write_output_file(path, i)
