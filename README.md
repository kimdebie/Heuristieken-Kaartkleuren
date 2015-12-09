# Heuristieken

Modules:

Init_net:
Functions and classes required to initiate the network from the provided csv file

	Functions:
		load_dict(filename)
			Loads csv-map data into dictionary.
			Requires a csv filename of the file containing the network friends data.
			Returns a dictionary with node# as keys, array of friends node# as values.
		
		initiate(dict_countries)
			Returns a list of country-objects.

	Classes:
		Country
			Definition of country object.


Initiation_map:
Functions and classes required to initiate the list of countries from the provided csv file

	Functions:
		load_dict(filename)
			Loads csv-map data into dictionary.
			Requires a csv filename of the file containing the maps countries and adjacent countries.
			Returns a dictionary with countries as keys, array of adjacent countries as values.
		
		initiate(dict_countries)
			Returns a list of country-objects.

	Classes:
		Country
			Definition of country object.


