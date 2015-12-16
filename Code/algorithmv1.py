"""
" algorithmv1.py
" 
" Depth first search for a solution with a preset amount of colors.
" Order of coloring countries is all random.
" Will find a solution if there is one, but might take a little while.
"
" UvA - Minor Programmeren - Heuristieken 
" Kaartkleuren
" Team Mushroom
" Kim de Bie, Jeroen de Jong, Rik Volger 
"""

import random 
import copy
import time


'''
' Determines which country will be the basis for creating children.
' Will take a random country out of the list. 
' Continues to do so untill a country is selected that is not already coloured.
' Returns the country-object from the dictionary countries_object.
'''
def next_child(parent, countries_object):

    countrynames = []

    # place all colored countries in the array countrynames
    for country in parent:
        countrynames.append(country.country_name)

    # generates random key
    key = random.choice(countries_object.keys())

    # if key is in already colored countries, selects a new key untill uncolored country is selected
    while key in countrynames:
        key = random.choice(countries_object.keys())

    # return the country object from the countries_object dictionary.
    return countries_object[key]

'''
' Generates next generation of children in all possible colors.
' 
' Will get the country to base the children on from a cal to next_child().
' Updates this country's available colors based on the already colored adjacent countries.
' Then creates children for all available colors.
' 
' Returns a list of the created children. If no children created, the list will be empty.
'''
def generate_children(parent, countries_object):
    # create placeholder for children
    children = []

    # call next_child(), passing the passed parent and countries_object
    next_country = next_child(parent, countries_object)

    # using the country's inherent function to update available colours, update
    next_country.update_available_colours(parent)

    # create a child for every color still available
    for colour in next_country.available_colours:
        
        # create a copy using copy module, so we don't use references to the original
        copy_parent = copy.copy(parent)
        copy_next_country = copy.copy(next_country)

        # create child with selected colour from available_colours
        copy_next_country.current_colour = colour
        copy_next_country.is_coloured = True

        # create a combination of the copied parent and new child
        copy_parent.append(copy_next_country)
        
        # append combination to the list of children.
        children.append(copy_parent)
   
    # update status of country in countries_object to colored 
    next_country.is_coloured = True

    # reset available colours to all, needed if we will color the same area again
    next_country.available_colours = ["red", "green","yellow","blue"]

    # return the array of all created children
    return children

'''
' Orchestrates the creation of children and keeps track of the stack.
' 
' Needs the countries_object dictionary as an argument.
' Will color the first country.
' Generates new random seeds for the random selection.
' 
' Returns the array of country objects of the solution if found.
' If no solution is found, prints 'no solution', returns nothing.
'''
def algorithm(countries_object):
    # create placeholder for solution
    solution = []

    # initializing stack
    stack = []

    # choose first random key
    key = random.choice(countries_object.keys())

    # create 1 colored version the chosen country and append to stack
    colour = countries_object[key].available_colours[len(countries_object[key].available_colours) - 1]
    country = copy.copy(countries_object[key])
    country.current_colour = colour
    country.is_coloured = True
    stack.append([country])
    
    # create counter to generate random seeds.
    i = 1

    # while there is something in the stack, see if a solution can be found
    while (len(stack) != 0):
        
        # generate new random seed for choosing the next country
        random.seed(time.clock() + i)
        
        # update counter for the random seed
        i += 1

        # pop the last generated parent/state from the stack
        parent = stack.pop()

        # if this parent contains all countries, all countries were coloured
        # this means a solution was found.
        if len(parent) == len(countries_object):
            return parent
        
        children = generate_children(parent, countries_object)

        # if there are no children, no need to append them
        if len(children) != 0:
            # all created children could lead to a solution, append them to stack
            for child in children:
                stack.append(child)

    # if the stack is empty, there are no solutions
    if len(stack) == 0:
        print "No solution"