import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import dwave_networkx as dnx
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
            else:
                row[i] = int(row[i])
        adj_mat.append(row)

    graph = su.adjacency_matrix_to_graph(adj_mat)[0]
    nx.draw(graph)
    plt.savefig("filename.png")

    return graph, home_names, starting_point

def shortest_paths(G, start_node, target):
    paths = nx.shortest_path(G, start_node, target)
    return paths

def get_shortest_path(G, start_node, homes):
    origin = start_node
    path = [start_node]
    while homes != []:
        temp_paths = []
        for h in homes:
            temp_paths.append(shortest_paths(G, start_node, h))
        temp_paths.sort(key=len)

        chosen_path = temp_paths[0]
        print(chosen_path)

        path.extend(temp_paths[0][1:])
        destination = temp_paths[0][-1]
        homes.remove(destination)
        start_node = destination
    return_home = shortest_paths(G, start_node, origin)
    path.extend(return_home[1:])
    print(path)
    return path

def write_output_file(path, size, origin, list_of_homes):
    checkpoints = set(path)
    # print(list_of_homes)

    path_str_list = [str(p) for p in path]
    path_str = ' '.join(path_str_list)
    file = open(f'{size}.out',"w")
    file.write("{0}\n".format(path_str))
    # print(path_str)

    file.write("{0}\n".format(len(list_of_homes)))
    # print(len(list_of_homes))

    for h in checkpoints:
        if h in list_of_homes:
            drop_off = str(h) + ' ' + str(h)
            # print(drop_off + '\n')
            file.write("{0}\n".format(drop_off))

    file.close()

for i in [200]:
    (G, homes, start_node) = create_graph(f'{i}.in')
    original_homes = homes.copy()
    path = get_shortest_path(G, start_node, homes)
    write_output_file(path, i, start_node, original_homes)
    print(G.edges())
