# what map are we using? {'spain', 'india', 'USA'}
my_map = 'USA'

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

# load the dictionary
dict_countries = importvis.load_dict(my_map)

# --------------------- Making a class for the countries. --------------------- #

class country(object):

    def __init__(self, key):
        self.available_colours = []
        self.current_colour = ""
        self.is_coloured = False
        self.amount_adjacent = 0
        self.country_name = key
        # list with all the adjacent countries as objects.
        self.adjacent_countries = list()

    # set the adjecent countries for this country and determine length
    def add_adjacent_countries(self,adj_country_list,countries_object):
        for entry in adj_country_list:
            self.adjacent_countries.append(countries_object[entry])

        # determine length
        self.amount_adjacent = len(adj_country_list)

    # updates the available_colours for the country based on current_colour
    # of the adjacent_countries coloured in current situation (parent).
    def update_available_colours(self, parent):
        for country in parent:
            if country.is_coloured: #and len(self.available_colours) != 0:
                for adjacent_country in self.adjacent_countries:
                    if country.country_name == adjacent_country.country_name and country.current_colour in self.available_colours:
                        self.available_colours.remove(country.current_colour)

# -------------------------------- initiation --------------------------------- #

def GetColourArray(number):
    color_array = ["red", "green","yellow","blue","purple","pink","orange"]
    return color_array[:number]

def get_starting_number():
	"""
	make an underestimation of where to start the algorithm
	"""

	max_amount = 0

	# Get the min colors needed.
	for entry in countries_object:
		test = countries_object[entry]
		for entry2 in test.adjacent_countries: #get into the adjacent countries
			amount = len(set(entry2.adjacent_countries) & set(test.adjacent_countries))
			if max_amount < amount:
				max_amount = amount

	if max_amount < 2:
		max_amount = 2

	return max_amount


# dictionary with all the country objects.
countries_object = dict()

# make the dictionary with all the objects.
# first, without adjecent country objects
for key in dict_countries:
    countries_object[key] = country(key)

# add the adjacent_countries to the object.
# now add these objects
for key in countries_object:
    countries_object[key].add_adjacent_countries(dict_countries[key],countries_object)

# add the colours
for key in countries_object:
    countries_object[key].available_colours = GetColourArray(get_starting_number())
    print countries_object[key].available_colours

# update the color array.
counter = 0
def get_correct_number():
    globals()['counter'] += 1
    return get_starting_number() + globals()['counter']


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

    # if no country with 1 possibility is present, select random
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
    next_country.available_colours = GetColourArray(get_starting_number() + globals()['counter'])

    return children

def all_countries_coloured(countries_object):
    for country in countries_object:
        if countries_object[country].is_coloured == False:
            return False
    return True

def algorithm():

    solution = []
    print "starting the algo"
    # depth-first
    while (len(stack) != 0):
        # new random seed for selecting next country
        parent = stack.pop()

        #print len(parent)
        #print len(countries_object)
        if len(parent) == len(countries_object):
            solution = parent
            break
        children = generate_children(parent)
        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            for child in children:
                stack.append(child)

    # if the stack is empty, there are no solutions
    if len(stack) == 0:

        # add 1+ color to the country objects
        GoodNumberOne = get_correct_number()

        for key in countries_object:
            countries_object[key].available_colours = GetColourArray(GoodNumberOne)
            print countries_object[key].available_colours

        # initial situation
        for colour in countries_object[countries_object.keys()[0]].available_colours:
            country = copy.copy(countries_object[countries_object.keys()[0]])
            country.current_colour = colour
            country.is_coloured = True
            stack.append([country])

        # rerun the algorithm with +1 colour
        return algorithm()
    else:
        print solution
        return solution

solution = algorithm()

for entry in solution:
    print entry.country_name, entry.current_colour

# draw the map
importvis.Draw_map(solution,my_map)
