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

print_input(50, 25)
