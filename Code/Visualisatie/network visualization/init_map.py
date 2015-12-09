
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
                        self.available_colours.remove(country.current_colour)

# -------------------------------- initiation --------------------------------- #

def initiate(dict_countries):
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

    return countries_object
