

# ----------------------- part to import the dictionary. ---------------------- #
import copy
import csv
import timeit
import numpy
import time
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
dict_countries = load_dict("Map3.csv")

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
        copy_parent = copy.copy(parent)
        copy_next_country = copy.copy(next_country)

        # only creates children that can be created (i.e. that have an available color)
        copy_next_country.current_colour = colour
        copy_next_country.is_coloured = True
        # add copy to stack entry, save new entry on stack
        copy_parent.append(copy_next_country)
        children.append(copy_parent)
        #print copy_next_country.country_name, '+', copy_next_country.current_colour

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
        random.seed(time.clock() + i)
        i += 1

        parent = stack.pop()

        #print len(parent)
        #print len(countries_object)
        if len(parent) == len(countries_object):
            print 'found!'
            solution = parent
            break
        
        children = generate_children(parent)
        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            for child in children:
                stack.append(child)

    # if the stack is empty, there are no solutions
    if len(stack) == 0:
        print "No solution"
    #else:
        #print solution

#--------------------return the timing of the results--------------------------------------------#
averages = []
for i in range(0,100):
    times = []
    for i in range(0,100):
        start = timeit.default_timer()
        algorithm();
        end = timeit.default_timer() - start
        times.append(end)

    #print max(times), min(times), numpy.mean(times)
    averages.append(numpy.mean(times))

#--------------------------display results in histogram------------------------------------------#
'''
Creating a histogram, edited from http://matplotlib.org/1.5.0/examples/animation/histogram.html 
'''
"""
This example shows how to use a path patch to draw a bunch of
rectangles for an animated histogram
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

fig, ax = plt.subplots()

# histogram our data with numpy
data = averages
n, bins = numpy.histogram(data, 100)

# get the corners of the rectangles for the histogram
left = numpy.array(bins[:-1])
right = numpy.array(bins[1:])
bottom = numpy.zeros(len(left))
top = bottom + n
nrects = len(left)

# here comes the tricky part -- we have to set up the vertex and path
# codes arrays using moveto, lineto and closepoly

# for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
# CLOSEPOLY; the vert for the closepoly is ignored but we still need
# it to keep the codes aligned with the vertices
nverts = nrects*(1 + 3 + 1)
verts = numpy.zeros((nverts, 2))
codes = numpy.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

barpath = path.Path(verts, codes)
patch = patches.PathPatch(
    barpath, facecolor='red', edgecolor='purple', alpha=0.5)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())


def animate(i):
    # simulate new data coming in
    data = averages
    n, bins = numpy.histogram(data, 100)
    top = bottom + n
    verts[1::5, 1] = top
    verts[2::5, 1] = top
    return [patch, ]

ani = animation.FuncAnimation(fig, animate, 1, repeat=False, blit=True)
plt.show()