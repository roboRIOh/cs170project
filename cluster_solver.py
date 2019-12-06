import math
import random
from gurobipy import *
# import sys
# sys.path.append('..')
# sys.path.append('../..')
# import argparse
# import utils
#
# from student_utils import *
# """
# ======================================================================
#   Complete the following function.
# ======================================================================
# """
#
# def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
#     """
#     Write your algorithm here.
#     Input:
#         list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
#         list_of_homes: A list of homes
#         starting_car_location: The name of the starting location for the car
#         adjacency_matrix: The adjacency matrix from the input file
#     Output:
#         A list of locations representing the car path
#         A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
#         NOTE: both outputs should be in terms of indices not the names of the locations themselves
#     """
#     pass
#
# """
# ======================================================================
#    No need to change any code below this line
# ======================================================================
# """
#
# """
# Convert solution with path and dropoff_mapping in terms of indices
# and write solution output in terms of names to path_to_file + file_number + '.out'
# """
# def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
#     string = ''
#     for node in path:
#         string += list_locs[node] + ' '
#     string = string.strip()
#     string += '\n'
#
#     dropoffNumber = len(dropoff_mapping.keys())
#     string += str(dropoffNumber) + '\n'
#     for dropoff in dropoff_mapping.keys():
#         strDrop = list_locs[dropoff] + ' '
#         for node in dropoff_mapping[dropoff]:
#             strDrop += list_locs[node] + ' '
#         strDrop = strDrop.strip()
#         strDrop += '\n'
#         string += strDrop
#     utils.write_to_file(path_to_file, string)
#
# def solve_from_file(input_file, output_directory, params=[]):
#     print('Processing', input_file)
#
#     input_data = utils.read_file(input_file)
#     num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
#     car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)
#
#     basename, filename = os.path.split(input_file)
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)
#     output_file = utils.input_to_output(input_file, output_directory)
#
#     convertToFile(car_path, drop_offs, output_file, list_locations)
#
#
# def solve_all(input_directory, output_directory, params=[]):
#     input_files = utils.get_files_with_extension(input_directory, 'in')
#
#     for input_file in input_files:
#         solve_from_file(input_file, output_directory, params=params)
#
#
# if __name__=="__main__":
#     parser = argparse.ArgumentParser(description='Parsing arguments')
#     parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
#     parser.add_argument('input', type=str, help='The path to the input file or directory')
#     parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
#     parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
#     args = parser.parse_args()
#     output_directory = args.output_directory
#     if args.all:
#         input_directory = args.input
#         solve_all(input_directory, output_directory, params=args.params)
#     else:
#         input_file = args.input
#         solve_from_file(input_file, output_directory, params=args.params)


# Callback - use lazy constraints to eliminate sub-tours

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

# Create n random points
#
# random.seed(1)
# points = []
# for i in range(n):
#   points.append((random.randint(0,100),random.randint(0,100)))
#
# m = Model()

def TSP(home_distances):
    # Create variables

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
    print(selected)
