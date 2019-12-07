import os
import sys
sys.path.append('..')
sys.path.append('../..')
sys.path.append('/Library/Python/2.7/site-packages/')
import argparse
import utils
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import dwave_networkx as dnx
from student_utils import *

import math
import random
from gurobipy import *

"""
======================================================================
  Complete the following function.
======================================================================
"""
# GLOBAL VARIABLE
n = 10 # Used in tour optimization
starting_car_index = 0

def print_2d_array(array):
    print('\n'.join(' '.join(str(x) for x in row) for row in array))

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

def vertex_path(adjmat):
  G = create_graph(adjmat, 'graph')
  edgelist = list(nx.dfs_edges(G, source=starting_car_index))
  vertexlist = [starting_car_index]
  # return G,[starting_car_index] + [i[1] for i in edgelist] + [starting_car_index]
  return G, edgelist

def create_graph(adjacency_matrix, name):
    graph = adjacency_matrix_to_graph(adjacency_matrix)[0]
    nx.draw(graph)
    plt.savefig(f'{name}.png')
    plt.clf()

    return graph

def shortest_path(G, start_node, target):
    path = nx.shortest_path(G, start_node, target)
    return path

def construct_cycle(adjacency_matrix, source):
    # Given an adjacency matrix of a TSP solution, output a possible cycle to take
    return nx.find_cycle(adjacency_matrix_to_graph(adjacency_matrix)[0], source)

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    blockPrint()

    home_indices_dict = {} # Dictionary of homes, where each entry is (key=index:value=name of home)
    home_indices = [] # List of indices where homes are located
    home_indices_and_source = [] # List of indices where homes are located and the source node
    location_indices = [i for i in range(len(list_of_locations))] # List of indices of all locations
    global starting_car_index
    starting_car_index = list_of_locations.index(starting_car_location)
    starting_car_index_TSP = 0
    drop_off_dict = {}

    for i in range(len(list_of_locations)):
        loc = list_of_locations[i]
        if loc in list_of_homes:
            home_indices_dict[i] = list_of_locations[i]
            home_indices.append(i)
            home_indices_and_source.append(i)
        elif loc == starting_car_location:
            home_indices_and_source.append(i)
            starting_car_index_TSP = home_indices_and_source.index(i)

    print(starting_car_index)
    print('homes')
    print(home_indices)
    print(home_indices_dict)

    G = create_graph(adjacency_matrix, 'graph')
    print_2d_array(adjacency_matrix)

    # 2D array where each value shortest_paths[i][j] is the shortest path from i to j where i and j are homes
    shortest_paths = [[nx.shortest_path(G, i, j) for j in home_indices_and_source] for i in home_indices_and_source]
    print_2d_array(shortest_paths)
    # 2D array where each value shortest_path_length[i][j] is the length of the shortest path from i to j where i and j are homes
    shortest_paths_lengths = [[nx.shortest_path_length(G, i, j) for j in home_indices_and_source] for i in home_indices_and_source]

    if (len(home_indices) == 1):
        car_path = []
        drop_off_dict[starting_car_index] = home_indices
    else:
        print("Shortest Paths Lengths Matrix")
        print_2d_array(shortest_paths_lengths)
        sol,TSP_path = TSP(shortest_paths_lengths)
        selected_adjacency_matrix = [[0 for i in range(n)] for i in range(n)]
        TSP_shortest_paths = [[[] for i in range(n)] for i in range(n)]
        for t in TSP_path:
            x, y = t
            selected_adjacency_matrix[x][y] = 1
            selected_adjacency_matrix[y][x] = 1
            TSP_shortest_paths[x][y] = shortest_paths[x][y]
            TSP_shortest_paths[y][x] = shortest_paths[y][x]
        print_2d_array(selected_adjacency_matrix)
        print("TSP_shortest_paths")
        print_2d_array(TSP_shortest_paths)

        home_cycle = construct_cycle(selected_adjacency_matrix, starting_car_index_TSP)
        print('home_cycle')
        print(home_cycle)

        TSP_shortest_paths_am = [['x' for i in range(len(adjacency_matrix))] for i in range(len(adjacency_matrix))]
        for i in range(len(TSP_shortest_paths)):
            for j in range(len(TSP_shortest_paths)):
                path = TSP_shortest_paths[i][j]
                p_length = len(TSP_shortest_paths[i][j])
                if p_length > 1:
                    for x in range(p_length - 1):
                        node_1 = path[x]
                        node_2 = path[x + 1]
                        TSP_shortest_paths_am[node_1][node_2] = adjacency_matrix[node_1][node_2]
        print_2d_array(TSP_shortest_paths_am)

        shortest_path_expanded = []
        for xy in home_cycle:
            x, y = xy
            shortest_path_expanded.append(TSP_shortest_paths[x][y])
        print('shortest path expanded')
        print(shortest_path_expanded)

        concat = [starting_car_index]
        for i in shortest_path_expanded:
            concat += i[1:]
        print(concat)
        solution_path = []
        for i in range(len(concat)-1):
            solution_path.append((concat[i],concat[i+1]))
        print(solution_path)

        # enablePrint()

        
        sol_path = solution_path
        i = 0
        while (i != len(sol_path)-1 and i != -1):
            # print(sol_path[i][0], sol_path[i+1][1])
            print(i,len(sol_path))
            if (sol_path[i][0] == sol_path[i+1][1]):
                # print(i, len(sol_path))
                if (len(sol_path) == 2):
                    sol_path_new = [(starting_car_index,starting_car_index)]
                else:
                    sol_path_new = sol_path[:i] + sol_path[i+2:]

                if (sol_path[i][1] in home_indices_dict):
                    if (sol_path[i][0] in drop_off_dict):
                        drop_off_dict[sol_path[i][0]] += [sol_path[i][1]]
                    else:
                        drop_off_dict[sol_path[i][0]] = [sol_path[i][1]]
                if (sol_path[i][1] in drop_off_dict):
                    if (sol_path[i][0] in drop_off_dict):
                        drop_off_dict[sol_path[i][0]] += drop_off_dict.get(sol_path[i][1])
                    else:
                        drop_off_dict[sol_path[i][0]] = drop_off_dict.get(sol_path[i][1])
                    del drop_off_dict[sol_path[i][1]]

                sol_path = sol_path_new.copy()
                i -= 1
            else:
                # print(sol_path[i][0], sol_path[i][0] in home_indices)
                if (sol_path[i][0] in home_indices):
                    if (not sol_path[i][0] in drop_off_dict):
                        drop_off_dict[sol_path[i][0]] = [sol_path[i][0]]
                i += 1
        print(i, len(sol_path))
        if (sol_path[i][0] in home_indices):
            if (not sol_path[i][0] in drop_off_dict):
                drop_off_dict[sol_path[i][0]] = [sol_path[i][0]]

        

        car_path = [starting_car_index]
        for i in sol_path:
          car_path.append(i[1])

    print("Solution Path:",car_path)
    print("Drop off Locations:",drop_off_dict)

    count = 0
    for i in drop_off_dict:
        count += len(drop_off_dict[i])
    print(home_indices)
    print(len(home_indices), count)

    return car_path, drop_off_dict


    # walk_tot = 0
    # drop_off_dict = {}
    # ph = TSP_path_of_homes
    # pl = TSP_path_includ_loc_between
    # Gh = G_homes
    # Gl = G_locs
    # h = 1 #indicies counter for ph
    # l = 1 #indicies counter for pl
    # while(h != len(ph) - 1):
    #     curr_to_next = nx.shortest_path_length(Gl,source=pl[l],target=pl[l+1])
    #     prev_to_curr = nx.shortest_path_length(Gl,source=pl[l-1],target=pl[l])
    #     next_to_prev = nx.shortest_path_length(Gl,source=pl[l+1],target=pl[l-1])
    #     print("ph:")
    #     print(ph)
    #     print("pl:")
    #     print(pl)
    #     if (curr_to_next >= next_to_prev + prev_to_curr):
    #         ph[h+1] = pl[l-1]
    #         if (pl[l-1] in drop_off_dict):
    #             drop_off_dict[pl[l-1]].append(pl[l])
    #         else:
    #             drop_off_dict[pl[l-1]] = [pl[l]]
    #         if (pl[l] in drop_off_dict):
    #             drop_off_dict[pl[l-1]].append(drop_off_dict.get(pl[l]))
    #         walk_tot += next_to_prev + prev_to_curr

    #         ph_new = [starting_car_index]
    #         for i in range(len(ph)-1):
    #             if (ph[i] in list_of_homes and ph[i+1] in list_of_homes):
    #                 ph_new += shortest_paths[ph[i]][ph[i+1]][1:]
    #             else:
    #                 ph_new += nx.shortest_path(Gl,ph[i],ph[i+1])[1:]
    #         ph = ph_new.copy()

    #         if (ph[h] == ph[h+1]):
    #             ph.pop(h+1)
    #     else:
    #         l += 1
    #         if (ph[l] in ph):
    #           h += 1
"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)
    
    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    i = 0
    l = len(input_files)
    for input_file in input_files:
        enablePrint()
        print("Currently Solving:", i, " / ", l, " : ", input_file)
        i += 1
        ofile = "outputs/" + input_file[7:-2] + "out"
        if (not os.path.isfile(ofile)): 
            solve_from_file(input_file, output_directory, params=params)


# Gurobi LP TSP solver
def subtourelim(model, where):
  if where == GRB.callback.MIPSOL:
    selected = []
    # make a list of edges selected in the solution
    for i in range(n):
      sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
      selected += [(i,j) for j in range(n) if sol[j] > 0.5]
    # find the shortest cycle in the selected edge list
    tour = subtour(selected)
    if len(tour) < n:
      # add a subtour elimination constraint
      expr = 0
      for i in range(len(tour)):
        for j in range(i+1, len(tour)):
          expr += model._vars[tour[i], tour[j]]
      model.cbLazy(expr <= len(tour)-1)


# Euclidean distance between two points

def distance(points, i, j):
  dx = points[i][0] - points[j][0]
  dy = points[i][1] - points[j][1]
  return math.sqrt(dx*dx + dy*dy)


# Given a list of edges, finds the shortest subtour

def subtour(edges):
  visited = [False]*n
  cycles = []
  lengths = []
  selected = [[] for i in range(n)]
  for x,y in edges:
    selected[x].append(y)
  while True:
    current = visited.index(False)
    thiscycle = [current]
    while True:
      visited[current] = True
      neighbors = [x for x in selected[current] if not visited[x]]
      if len(neighbors) == 0:
        break
      current = neighbors[0]
      thiscycle.append(current)
    cycles.append(thiscycle)
    lengths.append(len(thiscycle))
    if sum(lengths) == n:
      break
  return cycles[lengths.index(min(lengths))]

def TSP(home_distances):
    # Create variables
    m = Model()
    global n
    n = len(home_distances)

    vars = {}
    for i in range(n):
       for j in range(i+1):
         vars[i,j] = m.addVar(obj=home_distances[i][j], vtype=GRB.BINARY,
                              name='e'+str(i)+'_'+str(j))
         vars[j,i] = vars[i,j]
       m.update()

    # Add degree-2 constraint, and forbid loops
    for i in range(n):
      m.addConstr(quicksum(vars[i,j] for j in range(n)) == 2)
      vars[i,i].ub = 0
    m.update()

    # Optimize model
    m._vars = vars
    m.params.LazyConstraints = 1
    m.optimize(subtourelim)

    solution = m.getAttr('x', vars)
    selected = [(i,j) for i in range(n) for j in range(n) if solution[i,j] > 0.5]
    assert len(subtour(selected)) == n
    return solution,selected

# Main script from CS170 course source code
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = 'outputs'
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
