
import csv

# Loads a dictionary from a comma-separated-values file
# Returns a dictionary with area names as keys and neighbours as values
def load_dict(my_map):

    if my_map in ['india', 'spain', 'USA']:
        if my_map == 'india':
            filename = "Dictionary/Map1.csv"

        elif my_map == 'spain':
            filename = "Dictionary/Map2.csv"

        elif my_map == 'USA':
            filename = "Dictionary/Map3v2.csv"
        else:
            sys.exit("unknown map, please check top of the code!")

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

    elif my_map in ['network1', 'network2', 'network3', 'network4']:
        if my_map == 'network1':
            filename = "Dictionary/Network1.csv"

        elif my_map == 'network2':
            filename = "Dictionary/Network2.csv"

        elif my_map == 'network3':
            filename = "Dictionary/Network3.csv"

        elif my_map == 'network4':
            filename = "Dictionary/Network3.csv"

        # open provided file
        countries_csv = open(filename, 'r')

        # initiate reader for the csv file
        reader = csv.reader(countries_csv, delimiter=';')
        reader.next()

        # create dictionary
        countries = dict()

        # read all rows of csv_file
        for row in reader:
            # take first value of row as key in dictionary
            # add rest of list as value in dictionary
            try:
                if not row[1] in countries[row[0]]:
                    countries[row[0]].append(row[1])
            except (AttributeError, KeyError):
                countries[row[0]] = list()
                countries[row[0]].append(row[1])
            try:
                if not row[0] in countries[row[1]]:
                    countries[row[1]].append(row[0])
            except (AttributeError, KeyError):
                countries[row[1]] = list()
                countries[row[1]].append(row[0])

        # return written dictionary
        return countries
    
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
                        self.available_colours.remove(country.current_colour)

# ------------------------ Update minimum colours ---------------------------- #

def GetColourArray(number):
    color_array = ["red", "green","yellow","blue","purple","pink","orange"]
    return color_array[:number]

def get_starting_number(countries_object):
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

# ------------------------------ Initiation ---------------------------------- #
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

    # add the colours
    for key in countries_object:
        countries_object[key].available_colours = GetColourArray(get_starting_number(countries_object))
        print countries_object[key].available_colours

    return countries_object
