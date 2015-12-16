


# what type of data are we using?
    # maps :['spain', 'india', 'USA']
    # network : ['network1', 'network2', 'network3']

my_map = 'network3'

# ------------------------------ Import libraries ----------------------------- #

import sys
import random
import copy

# timing the algorithm + results
import timeit
import time
import numpy

# import the visualisation and csv importer
import importvis
import init_map

# load the dictionary
dict_countries = init_map.load_dict(my_map)

# create list of countries
countries_object = init_map.initiate(dict_countries,my_map)

# update the color array.
counter = -1
StartingpointNumb = init_map.get_starting_number(countries_object,my_map)
def get_correct_number():
    globals()['counter'] += 1
    return StartingpointNumb + globals()['counter']

print StartingpointNumb

StartingColours = init_map.GetColourArray(get_correct_number())

print StartingColours

# returns StartingColours
def return_startingColours():
    return copy.copy(StartingColours)



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
    # print "child creating", return_startingColours(),temp_numb
    next_country.is_coloured = True
    next_country.available_colours = return_startingColours()
    # print "child born", return_startingColours(),temp_numb


    return children

def all_countries_coloured(countries_object):
    for country in countries_object:
        if countries_object[country].is_coloured == False:
            return False
    return True


def algorithm():

    steps = 0

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
    for colour in countries_object[key].available_colours:
        country = copy.copy(countries_object[key])
        country.current_colour = colour
        country.is_coloured = True
        stack.append([country])

    solution = []

    # depth-first
    while (len(stack) != 0):
        # new random seed for selecting next country
        parent = stack.pop()

        #print len(parent)
        #print len(countries_object)
        if len(parent) == len(countries_object):
            #if you want the solution as output
            solution = parent
            #if you want the amount of steps taken as output
            #solution = steps
            break

        children = generate_children(parent)

        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            steps += len(children)
            for child in children:
                stack.append(child)

    # if the stack is empty, there are no solutions
    if len(stack) == 0:

        print return_startingColours()
        print

        # StartingColours =
        globals()['StartingColours'] = init_map.GetColourArray(get_correct_number())

        print return_startingColours()
        for key in countries_object:
            countries_object[key].available_colours = return_startingColours()

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

solution = algorithm()

# draw the map
importvis.Visualize(solution,my_map)
