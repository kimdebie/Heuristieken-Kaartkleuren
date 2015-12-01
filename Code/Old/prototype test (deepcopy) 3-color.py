

# ----------------------- part to import the dictionary. ---------------------- #

import csv
# Loads a dictionary from a comma-separated-values file
# Returns a dictionary with area names as keys and neighbours as values
def load_dict(filename):
	# open provided file
	countries_csv = open(filename, 'r')

	# initiate reader for the csv file
	reader = csv.reader(countries_csv)

	# create dictionary
	countries = dict()

	# read all rows of csv_file
	for row in reader:
		# take first value of row as key in dictionary
		# add rest of list as value in dictionary
		countries[row[0]] = row[1:len(row)]

	# return written dictionary
	return countries

# call the load_dict function
dict_countries = load_dict("Map1.csv")

# --------------------- Making a class for the countries. --------------------- #

class country(object):

    def __init__(self, key):
        self.available_colours = ["red", "green","yellow"]
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
            if country.is_coloured and country.current_colour in self.available_colours:
                for adjacent_country in self.adjacent_countries:
                    if country.country_name == adjacent_country.country_name:
                        #print 'removing', country.current_colour, 'from', country.country_name
                        self.available_colours.remove(country.current_colour)

# -------------------------------- initiation --------------------------------- #

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

# ------------------------ part to do the calculating ------------------------- #

# there is a separate calculation file - this is 'prototype depth-first smart.py'
# initializing stack
import random 
from copy import deepcopy

# initializing stack
stack = []


# initial situation
for colour in countries_object[countries_object.keys()[0]].available_colours:
    countries_object[countries_object.keys()[0]].current_colour = colour
    stack.append([countries_object[countries_object.keys()[0]]])

# what is the next child we look at?
def next_child(parent):

    countrynames = []

    for country in parent:
        countrynames.append(country.country_name)

    key = random.choice(countries_object.keys())

    while key in countrynames:
        key = random.choice(countries_object.keys())

    return countries_object[key]

# function to generate children
def generate_children(parent):
    children = []
    # for the last popped
    next_country = next_child(parent)

    # we only want to iterate over the colors that are available
    next_country.update_available_colours(parent)
    for colour in next_country.available_colours:
        # make copy - we want to add copies to stack, not references to originals
        copy_parent = deepcopy(parent)
        copy_next_country = deepcopy(next_country)

        # only creates children that can be created (i.e. that have an available color)
        copy_next_country.current_colour = colour
        copy_next_country.is_coloured = True
        # add copy to stack entry, save new entry on stack
        copy_parent.append(copy_next_country)
        children.append(copy_parent)
        #print copy_next_country.country_name, '+', copy_next_country.current_colour
    # save next country as coloured so that we won't pick it again   
    next_country.is_coloured = True
    next_country.available_colours = ["red", "green","yellow"]

    return children

def all_countries_coloured(countries_object):
    for country in countries_object:
        if countries_object[country].is_coloured == False:
            return False
    return True

solution = []

# depth-first
while (len(stack) != 0): #and all_countries_coloured(countries_object) == False):
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
            print child[len(child)-1].country_name, '+', child[len(child)-1].current_colour

# if the stack is empty, there are no solutions
if len(stack) == 0:
    print "No solution"
else:
    print solution



#   ****
#   ****
#   ****
#   ****
#   ****
#   ****
#   ****
#   ****
#    ****

# ----------------- part to do the displaying of the results ------------------ #








# part to display the return results.
