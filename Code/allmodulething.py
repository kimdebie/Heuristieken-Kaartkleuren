# what map are we using? {'spain', 'india', 'USA', 'network1', 'network2', 'network3'}
my_map = 'india'

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
import algorithmv1

# load the dictionary
dict_countries = init_map.load_dict(my_map)

# create list of countries
countries_object = init_map.initiate(dict_countries)

# update the color array.
counter = 0
def get_correct_number():
    globals()['counter'] += 1
    return init_map.get_starting_number(countries_object) + globals()['counter']

#--------------------return the timing of the results--------------------------------------------#

# steps = []

# for i in range(0,100):
#     step = algorithmv1.algorithm(countries_object)
#     print step
#     steps.append(step)
    
solution = algorithmv1.algorithm(countries_object)

# export the amount of steps taken to csv
#benchmark.exportcsv(steps)

# draw the map
importvis.Visualize(solution,my_map)
