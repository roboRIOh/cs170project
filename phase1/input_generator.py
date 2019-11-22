import numpy as np

# Input file format:
# 1 Number of locations
# 2 Number of homes
# 3 Names of locations
# 4 Names of homes
# 5 Name of starting point
# 6 Adjacency matrix

def print_input(locations, tas):
    # Prints specifications to input files based on locations and number of tas

    # Print line 1 and line 2 to file
    # print(locations, file = open("50.in", "a"))
    # print(tas, file = open("50.in", "a"))

    generate_names(locations, tas)

    # Generate random uniform x values for points.
    dist_x_array = np.random.uniform(0, 10, locations)
    # Generate random uniform y values for points.
    dist_y_array = np.random.uniform(0, 10, locations)

    print(dist_x_array)
    print(dist_y_array)

def generate_names(locations, tas):
    # Print names of locations (line 3) and names of homes (line 4) to
    # input file
    return

def generate_input(size):
    num_of_tas = size // 2 #arbitrary number to be determined
    home_numbers = np.arange(1,num_of_tas + 1 , 1)
    list_of_locations = ["location{0}".format(i+1) for i in range(size)]
    list_of_homes = [list_of_locations[np.random.randint(0,num_of_tas-1)] for i in range(num_of_tas)]
    adjmat = np.full((size,size),'x')
    for i in range(size):
        for j in range(i):
            x = set_edge()
            if (x != 0):
                adjmat[i][j] = x
                adjmat[j][i] = x
    file = open('{0}.out'.format(size),"w")
    file.write("{0}\n".format(size))
    file.write("{0}\n".format(num_of_tas))
    for i in range(size):
        file.write("{0} ".format(list_of_locations[i])) 
    file.write("\n")
    for i in range(num_of_tas):
        file.write("{0} ".format(list_of_homes[i])) 
    file.write("\n")
    file.write("{0}\n".format(list_of_locations[0]))
    for i in range(size):
        for j in range(size):
            file.write("{0} ".format(str(adjmat[i][j])))
        file.write("\n")

    file.close


def set_edge():
    return np.random.randint(0,2)

generate_input(50)
generate_input(100)
generate_input(200)
