
# what map are we using? {'spain', 'india', 'USA'}
my_map = 'USA'

# ------------------------------ Import libraries ----------------------------- #

# load and read the csv file.
import csv
import sys
import random
import copy
import timeit
import time

# is used to display the map
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon, PathPatch
import matplotlib.animation as animation

# get spain map working correctly with non english letters.
import unicodedata

# ----------------------- part to import the dictionary. ---------------------- #

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
if my_map == 'india':
	dict_countries = load_dict("../Dictionary/Map1.csv")

elif my_map == 'spain':
	dict_countries = load_dict("../Dictionary/Map2.csv")

elif my_map == 'USA':
	dict_countries = load_dict("../Dictionary/Map3.csv")

else:
	sys.exit("unknown map, please check top of the code!")


# --------------------- Making a class for the countries. --------------------- #

class country(object):

    def __init__(self, key):
        self.available_colours = ["red", "green","yellow", "blue"]
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
        #print countries_object[country].amount_adjacent
        if countries_object[country].amount_adjacent > countries_object[key].amount_adjacent and country not in countrynames:
            key = country

    #print countries_object[key].country_name
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
        #print copy_next_country.country_name, '+', copy_next_country.current_colour
    # save next country as coloured so that we won't pick it again
    next_country.is_coloured = True
    next_country.available_colours = ["red", "green","yellow", "blue"]

    return children

def all_countries_coloured(countries_object):
    for country in countries_object:
        if countries_object[country].is_coloured == False:
            return False
    return True

def algorithm():

    solution = []
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
            #for country in solution:
                #print country.country_name, country.current_colour, country.amount_adjacent
            break
        children = generate_children(parent)
        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            for child in children:
                stack.append(child)
                #print child[len(child)-1].country_name, '+', child[len(child)-1].current_colour

    # if the stack is empty, there are no solutions
    if len(stack) == 0:
        print "No solution"
    else:
        for country in solution:
                print country.country_name, country.current_colour, country.amount_adjacent
        return solution
        #print solution

solution = algorithm()
print solution


# initiate the dict to use outside the function
spain_dict = dict()

def what_map_to_use(my_map):
	# check what map is used!
	if my_map == "india":
		# ll means lowerleft, Northing and Easting, samen for Upper Right(UR)
		# as projection we're using mercator, the coordinate sytem used by the shapefiles.
		map = Basemap(llcrnrlon=69,llcrnrlat=23,urcrnrlon=79,urcrnrlat=30.3,
		             resolution='i', projection='merc')

		# read the geo shapefile.
		map.readshapefile('../JSON_files/Fixed_raj/IND_adm2', 'mkaart')
		return map

	elif my_map == 'spain':

		# compensate for the incorrect names on the spain map given by heuristieken.nl
		spain_dict.update({"jaen" : "lugo", "leon" : "a coruna","zamora" : "pontevedra","burgos" : "ourense","murcia" : "leon","guipuzcoa" : "asturias","toledo" : "zamora","pontevedra" : "salamanca","barcelona" : "caceres","madrid" : "badajoz","almeria" : "huelva","caceres" : "cadiz" ,"islas baleares" : "sevilla","albacete" : "malaga","las palmas" : "cordoba","valencia" : "ciudad real","cadiz" : "toledo","ciudad real" : "avila" ,"cantabria" : "valladolid","valladolid" : "palencia","guadalajara" :"cantabria","asturias" : "burgos","lugo": "segovia","huesca" : "la rioja","huelva" : "madrid","santa cruz de tenerife" : "jaen","zaragoza" : "granada","badajoz" : "soria","granada" : "guadalajara","sevilla" : "cuenca","vizcaya" : "albacete","cordoba" : "murcia","castellon" : "almeria","alava" : "alicante", "gerona" : "valencia","a coruna" : "teruel","salamanca" : "castellon","ourense" : "tarragona","alicante" : "zaragoza","navarra" : "navarra","segovia" : "alava","teruel" : "vizcaya","soria" : "guipuzcoa","malaga" : "huesca","tarragona" : "lleida","lleida" : "barcelona" ,"la rioja" : "girona"})

		map = Basemap(llcrnrlon=-10,llcrnrlat=35.2,urcrnrlon=4.3,urcrnrlat=44,
		             resolution='i', projection='merc')

		map.readshapefile('../JSON_files/Fixed_spaj/ESP_adm2', 'mkaart')
		return map

	elif my_map == 'USA':

		map = Basemap(llcrnrlon=-82,llcrnrlat=39,urcrnrlon=-74,urcrnrlat=42.5,
		             resolution='i', projection='merc')

		map.readshapefile('../JSON_files/Fixed_penns/USA_adm2', 'mkaart')
		return map
	# no need for else, because it is already checked at the create dictionary part.


# -------------------- part to do the displaying of the results ---------------------- #

# make the space to add the visualisation to.
figure = plt.figure()

# add a subplot 1 at position 1,1.
ax = figure.add_subplot(111)

# get shapefile
mkaart = what_map_to_use(my_map)

color_decoder = {"red" : "#a6cee3", "green" : "#1f78b4","yellow": "#b2df8a","blue" : "#33a02c", "purple" : "#fb9a99","pink" : "#e31a1c","orange" : "#fdbf6f" }

# animation function.  This is called sequentially
def animate():

	# the algorithm, see the algorithm function to add the algrotihm into.
    algorithm()

	# make empty array for the colored polygons.
    patches = []


	# empty the axis and remove them
    ax.clear()
    plt.axis('off')



	# add the color
	# if spain is not empty
    if my_map == 'spain':
        for key in spain_dict:
            for info, shape in zip(mkaart.mkaart_info, mkaart.mkaart):
                uni_string = unicode(info["NAME_2"],'utf8')
                uni_string = unicodedata.normalize('NFKD', uni_string ).encode('ascii', 'ignore')

                if uni_string.lower().find(spain_dict[key]) != -1:
                    patches.append(Polygon(np.array(shape), True))
                    ax.add_collection(PatchCollection(patches, facecolor=  countries_object[key].current_colour, edgecolor='k', linewidths=1., zorder=2))
                    patches = []


    else:
        for key in countries_object:
            for info, shape in zip(mkaart.mkaart_info, mkaart.mkaart):
                if info["NAME_2"].lower().find(countries_object[key].country_name) != -1:

                    patches.append(Polygon(np.array(shape), True))

                    for entry in solution:
                        if entry.country_name == key:
                            color = color_decoder[entry.current_colour]

                    ax.add_collection(PatchCollection(patches, facecolor= color, edgecolor='k', linewidths=1., zorder=2))
                    patches = []


# anim = animation.FuncAnimation(figure, animate, frames=200, interval=1, blit=False)

animate()

# show the animation
plt.show()
