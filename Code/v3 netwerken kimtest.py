

# ----------------------- part to import the dictionary. ---------------------- #
import random 
import copy
import time
import init_net
import csv

# call the load_dict function
dict_countries = init_net.load_dict("Network1.csv")

countries_object = init_net.initiate(dict_countries)

# ------------------------ part to do the calculating ------------------------- #


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
    next_country.available_colours = ["red", "green","yellow", "blue"]

    return children

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
    for colour in countries_object[key].available_colours:
        country = copy.copy(countries_object[key])
        country.current_colour = colour
        country.is_coloured = True
        stack.append([country])

    # depth-first
    while (len(stack) != 0):

        parent = stack.pop()
        if len(parent) == len(countries_object):
            solution = parent
            return solution

        children = generate_children(parent)

        # if there are no children, there are no solutions for this parent
        if len(children) != 0:
            for child in children:
                stack.append(child)

solution = algorithm()

with open('solutionfile.csv', 'wb') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(["connection", "color"])
    for connection in solution:
        row = [connection.country_name, connection.current_colour]
        writer.writerow(row)

import webbrowser
new = 2

url = "file:///C:/Users/Kim/Documents/GitHub/Heuristieken-Kaartkleuren/Code/Visualisatie/network%20visualization/d3.html"
webbrowser.open(url,new=new)