# Heuristieken/Programmeertheorie - Minor Programmeren - UvA
# Project group: Team Mushroom
# Creator: Rik Volger
# Contributors:

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
