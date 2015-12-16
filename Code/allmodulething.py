# what map are we using? {'spain', 'india', 'USA', 'network1', 'network2', 'network3'}
my_map = 'network3'

# what algorithm do we want to use? {'v1', 'v2', 'v3', 'v4'}
my_algo = 'v3'

# ------------------------------ Import libraries ----------------------------- #

import sys
import random
import copy

# timing the algorithm + results
import timeit
import numpy

# import the visualisation, csv importer and benchmark module
import importvis
import init_map
import benchmark

if my_algo == 'v1':
    import algorithmv1 as algo
elif my_algo == 'v2':
    import algorithmv2 as algo
elif my_algo == 'v3':
    import algorithmv3 as algo
elif my_algo == 'v4':
    import algorithmv4 as algo
else:
    sys.exit("Unvalid algorithm chosen, try again...")

# load the dictionary
dict_countries = init_map.load_dict(my_map)

# create list of countries
countries_object = init_map.initiate(dict_countries, my_algo)

# update the color array.
counter = 0
def get_correct_number():
    globals()['counter'] += 1
    return init_map.get_starting_number(countries_object) + globals()['counter']

#--------------------return the timing of the results--------------------------------------------#

'''
' Takes two arguments; count (an integer >0) and choice ('steps' or 'children')
' Runs count runs of the algorithm.
' 
' Will return an array of length count, containing the amount of steps taken or children created in each run
'''
def stepcounter(count, choice):

    if choice == 'steps':
        num = 1
    elif choice == 'children':
        num = 2
    else:
        sys.exit('stepcounter: Provide a valid choice, steps or children')

    if count < 1:
        sys.exit('stepcounter: Can\'t run less than 1 run, try again')

    steps = []

    for i in range(0,count):
        step = algo.algorithm(countries_object)[num]
        steps.append(step)

    return steps

solution = algo.algorithm(countries_object)[0]
steps = stepcounter(100, 'steps')

if solution:
    for country in solution:
        print country.country_name, ':', country.current_colour

# export the amount of steps taken to csv
#benchmark.exportcsv(steps)

# draw the map
# importvis.Visualize(solution,my_map)
