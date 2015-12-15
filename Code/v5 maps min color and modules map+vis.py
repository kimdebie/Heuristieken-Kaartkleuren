# what map are we using? {'spain', 'india', 'USA'}
my_map = 'spain'

# ------------------------------ Import libraries ----------------------------- #

import sys
import random
import copy

# timing the algorithm + results
import timeit
import time
import numpy

# import the visualisation, csv importer and benchmark module
import importvis
import init_map
import benchmark

# load the dictionary
dict_countries = init_map.load_dict(my_map)

# create list of countries
countries_object = init_map.initiate(dict_countries)


# update the color array.
counter = 0
def get_correct_number():
    globals()['counter'] += 1
    return init_map.get_starting_number(countries_object) + globals()['counter']


# ------------------------ part to do the calculating ------------------------- #

# initializing stack
stack = []

# initial situation
for colour in countries_object[countries_object.keys()[0]].available_colours:
    country = copy.copy(countries_object[countries_object.keys()[0]])
    country.current_colour = colour
    country.is_coloured = True
    stack.append([country])

# what is the next child we look at?
def next_child(parent):

    countrynames = []

    for country in parent:
        countrynames.append(country.country_name)

    key = random.choice(countries_object.keys())

    while key in countrynames:
        key = random.choice(countries_object.keys())

    for country in countries_object:
        if countries_object[country].amount_adjacent > countries_object[key].amount_adjacent and country not in countrynames:
            key = country

    return countries_object[key]

# function to generate children
def generate_children(parent):

    countrynames = []
    country_selected = False

    if len(parent) > 0:
        # store all countries from parent
        for country in parent:
            countrynames.append(country.country_name)

        # for all non-coloured countries
        for key in countries_object:
            if key not in countrynames:

                countries_object[key].update_available_colours(parent)

                # if 1 colour available, colour this country first
                if len(countries_object[key].available_colours) == 1:
                    next_country = countries_object[key]
                    country_selected = True

    # if no country with 1 possibility is present, select using algorithm for choice
    if not country_selected:
        next_country = next_child(parent)
        country_selected = True

    children = []

    # we only want to iterate over the colors that are available
    next_country.update_available_colours(parent)
    for colour in next_country.available_colours:
        # make copy - we want to add copies to stack, not references to originals
        copy_parent = copy.copy(parent)
        copy_next_country = copy.copy(next_country)

        # only creates children that can be created (i.e. that have an available color)
        copy_next_country.current_colour = colour
        copy_next_country.is_coloured = True
        # add copy to stack entry, save new entry on stack
        copy_parent.append(copy_next_country)
        children.append(copy_parent)

    # save next country as coloured so that we won't pick it again
    next_country.is_coloured = True
    next_country.available_colours = init_map.GetColourArray(init_map.get_starting_number(countries_object) + globals()['counter'])

    return children

def all_countries_coloured(countries_object):
    for country in countries_object:
        if countries_object[country].is_coloured == False:
            return False
    return True


def algorithm():

    # initiate counter for random seed
    i = 1

    # create stack as empty array
    stack = []

    # generate first key at random
    key = random.choice(countries_object.keys())

    # select country with most neighbours
    for country in countries_object:
        if countries_object[country].amount_adjacent > countries_object[key].amount_adjacent:
            key = country

    # colour first country
    country = copy.copy(countries_object[key])
    country.current_colour = country.available_colours[len(country.available_colours) - 1]
    country.is_coloured = True
    stack.append([country])

    # counter for steps, the first step has just been taken
    births = 1

    # counter for amount of children created, the first child has just been created.
    childrencreated = 1
    
    solution = []
    
    print "starting the algo"
    
    # depth-first
    while (len(stack) != 0):

        # new random seed for selecting next country
        random.seed(time.time() + i)
        i += 1

        # get parent from stack
        parent = stack.pop()

        #print len(parent)
        #print len(countries_object)
        if len(parent) == len(countries_object):
            # # if you want the solution as output
            #solution = parent
            # # if you want the amount of times children were created as output
            solution = births
            # # if you want the amount of children created as output
            # solution = childrencreated
            break
        children = generate_children(parent)
        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            births += 1
            childrencreated += len(children)
            for child in children:
                stack.append(child)

    # if the stack is empty, there are no solutions
    if len(stack) == 0:
        # add 1+ color to the country objects
        GoodNumberOne = get_correct_number()

        for key in countries_object:
            countries_object[key].available_colours = init_map.GetColourArray(GoodNumberOne)

        # initial situation
        for colour in countries_object[countries_object.keys()[0]].available_colours:
            country = copy.copy(countries_object[countries_object.keys()[0]])
            country.current_colour = colour
            country.is_coloured = True
            stack.append([country])

        # rerun the algorithm with +1 colour
        return algorithm()
    else:
        return solution

#solution = algorithm()

#--------------------return the timing of the results--------------------------------------------#

steps = []

for i in range(0,100):
    step = algorithm()
    print step
    steps.append(step)

    #print max(times), min(times), numpy.mean(times)
    
print steps

# export the amount of steps taken to csv
benchmark.exportcsv(steps)

# draw the map
#importvis.Visualize(solution,my_map,)
