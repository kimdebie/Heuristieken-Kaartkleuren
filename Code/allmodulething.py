


# what type of data are we using?
    # maps :['spain', 'india', 'USA']
    # network : ['network1', 'network2', 'network3']
my_map = 'india'

# what algorithm do we want to use? 
    # 'v1': random depth first
    # 'v2': random depht first, prioritizing countries with 1 colour available 
    # 'v3': adjacent-ordered depth first, prioritizing single colour-countries
    # 'v4': variable amount of starting colours, using v3
my_algo = 'v1'

# ------------------------------ Import libraries ----------------------------- #

import sys

# import the visualisation, csv importer and benchmark module
import importvis
import init_map
import benchmark

# import the algorithm chosen by user in the top section.
if my_algo == 'v1':
    import algorithmv1 as algo
elif my_algo == 'v2':
    import algorithmv2 as algo
elif my_algo == 'v3':
    import algorithmv3 as algo
elif my_algo == 'v4':
    import algorithmv4 as algo
else:
    sys.exit("Unvalid algorithm chosen, try again")

# -------------------------- Initiate network or map ------------------------- #

colour_list = ["red", "green", "yellow", "blue", "purple", "pink", "orange"]

# load the dictionary
dict_countries = init_map.load_dict(my_map)

# create list of countries
countries_object = init_map.initiate(dict_countries, my_map, my_algo, colour_list)

# find the minimum amount of colours needed
num_colours = init_map.get_starting_number(countries_object, my_map)

# -------------------- return the timing of the results -------------------------------------------- #

'''
' Takes two arguments; count (an integer >0) and choice ('steps' or 'children')
' Runs count runs of the algorithm.
' 
' Will return an array of length count, containing the amount of steps taken or children created in each run
'''
def stepcounter(count, choice):

    # validate user choice of type
    if choice == 'steps':
        num = 1
    elif choice == 'children':
        num = 2
    else:
        sys.exit('stepcounter: Provide a valid choice, steps or children')

    # validate user choice of runs
    if count < 1:
        sys.exit('stepcounter: Can\'t run less than 1 run, try again')

    steps = []

    # run the algorithm as often as asked
    for i in range(0,count):
        step = algo.algorithm(countries_object, num_colours, colour_list)[num]
        steps.append(step)

    # construct filename from chosen algorithm and map
    filename = my_algo + my_map

    # export data to csv
    benchmark.exportcsv(steps, filename)

# # draw the map
# solution = algo.algorithm(countries_object, num_colours, colour_list)[0]
# importvis.Visualize(solution,my_map)

# # export stepcounter to csv, either counting 'steps' or 'children'
# stepcounter(40, steps)