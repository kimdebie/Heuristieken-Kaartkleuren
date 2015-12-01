

# ----------------------- part to import the dictionary. ---------------------- #
import copy
import csv
import timeit
import time
import numpy
# Loads a dictionary from a comma-separated-values file
# Returns a dictionary with area names as keys and neighbours as values
def load_dict(filename):
    # open provided file
    csv_file = open(filename, 'r')

    # initiate reader for the csv file
    reader = csv.reader(csv_file, delimiter=';')
    reader.next()

    # create dictionary
    countries = dict()

    # read all rows of csv_file
    for row in reader:
        # take first value of row as key in dictionary
        # add rest of list as value in dictionary
        try:
            countries[row[0]].append(row[1])
        except (AttributeError, KeyError):
            countries[row[0]] = list()
            countries[row[0]].append(row[1])
        try:
            countries[row[1]].append(row[0])
        except (AttributeError, KeyError):
            countries[row[1]] = list()
            countries[row[1]].append(row[0])

    # return written dictionary
    return countries

# call the load_dict function
dict_countries = load_dict("Network1.csv")

# --------------------- Making a class for the countries. --------------------- #

class country(object):

    def __init__(self, key):
        self.available_colours = ["red", "green","yellow","blue"]
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
            if country.is_coloured:
                for adjacent_country in self.adjacent_countries:
                    if country.country_name == adjacent_country.country_name and country.current_colour in self.available_colours:
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
    next_country.available_colours = ["red", "green","yellow","blue"]

    return children

def all_countries_coloured(countries_object):
    for country in countries_object:
        if countries_object[country].is_coloured == False:
            return False
    return True

solution = []

def algorithm():
    i = 1
    # depth-first
    while (len(stack) != 0): #and all_countries_coloured(countries_object) == False):
        # new random seed for selecting next country
        random.seed(time.clock() + i)
        i += 1

        parent = stack.pop()
        #print len(parent)
        #print len(countries_object)
        if len(parent) == len(countries_object):
            solution = parent
            for country in solution:
                print country.country_name, country.current_colour
                for friend in country.adjacent_countries:
                    print friend.country_name
            return solution

        children = generate_children(parent)
        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            for child in children:
                stack.append(child)
                #print child[len(child)-1].country_name, '+', child[len(child)-1].current_colour

    # if the stack is empty, there are no solutions
    if len(stack) == 0:
        print "No solution"
    #else:
        #print solution

    return solution

# viz

import networkx as nx
import matplotlib.pyplot as plt

solution = algorithm()

friend_list = []
color_array = []
friend_connections = []
test = []
labels = {}

for country in solution:
    for friend in country.adjacent_countries:
        friend_connections.append([country.country_name,friend.country_name])
    friend_list.append(country.country_name)
    labels[country.country_name] = country.country_name
    color_array.append(country.current_colour)
    #print country.country_name, country.current_colour
    #print color_array


graph = nx.Graph()

# nodes are single elements
graph.add_nodes_from(friend_list)

#edges are the connections between them (so pairs of nodes)
graph.add_edges_from(friend_connections)

layout = nx.spring_layout(graph)

nx.draw_networkx_nodes(graph, pos=layout, node_color = color_array)
nx.draw_networkx_edges(graph, pos=layout, width=1.0,alpha=0.5)
nx.draw_networkx_labels(graph, pos=layout, labels=labels, font_size=16)

#nx.draw(graph, node_color = color_array)
print(graph.edges())
plt.show()
