import numpy as np
import networkx as nx

# Input file format:
# 1 Number of locations
# 2 Number of homes
# 3 Names of locations
# 4 Names of homes
# 5 Name of starting point
# 6 Adjacency matrix

def generate_input(size,x,y):
    num_of_tas = size // 2 #arbitrary number to be determined
    home_numbers = np.arange(1,num_of_tas + 1 , 1)
    list_of_locations = ["location{0}".format(i+1) for i in range(size)]
    list_of_homes = []
    while(len(list_of_homes) < num_of_tas):
        home = list_of_locations[np.random.randint(0,num_of_tas)]
        try:
            list_of_homes.index("{0}".format(home))
        except:
            list_of_homes.append(home)

    triG = nx.triangular_lattice_graph(x,y)
    triAdj = nx.adjacency_matrix(triG).toarray()
    adjmat = np.full((size,size),'x')
    for i in range(size):
        for j in range(i):
            x = triAdj[i,j]
            if (triAdj[i,j] != 0):
                adjmat[i][j] = x
                adjmat[j][i] = x

    file = open('{0}.in'.format(size),"w")
    file.write("{0}\n".format(size))
    file.write("{0}\n".format(num_of_tas))
    for i in range(size):
        file.write("{0} ".format(list_of_locations[i]))
    file.write("\n")
    for i in range(num_of_tas):
        file.write("{0} ".format(list_of_homes[i]))
    file.write("\n")
    file.write("{0}\n".format(list_of_locations[0]))
    for i in range(len(adjmat)):
        for j in range(len(adjmat[0])):
            file.write("{0} ".format(str(adjmat[i][j])))
        file.write("\n")

    file.close

def set_edge():
    return np.random.randint(0,2)

# generate_input(10,3,3)
generate_input(50,9,8)
generate_input(100,19,8)
generate_input(200,19,18)
