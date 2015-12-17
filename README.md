# Heuristieken

Readme.md
Gives an overview of the different modules, algorithms and other files found in the github directory Heuristieken-Kaartkleuren.
By: Kim de Bie, Jeroen de Jong & Rik Volger

/Code:
All source code and data needed for the algorithm.

	/Dictionary:
		The datafiles of the maps and networks, in csv format.

	/JSON_files:
		Files needed for the visualisation of the maps.

	/Network_files:
		Files specific for the network visualization.

	/Timelapse:
	A visualisation of the working algorithm, coloring countries one by one.

	Modules:

		Init_map:
		Functions and classes required to initiate the list of countries from the provided csv file

			Functions:
				load_dict(filename)
					Loads csv-map data into dictionary.
					Requires a csv filename of the file containing the network or map data.
					Returns a dictionary with node# or countries as keys, array of friends node# or adjacent countries as values.
				
				initiate(dict_countries)
					Returns a list of country-objects.

				GetColourArray(number)
					Returns an array of colours with length number. Maximum length is 7.

				get_starting_number(countries_object)
					Analyses the dictionary of countries and underestimates the minimum amount of colours needed to colour all countries.

			Classes:
				Country
					Definition of country object.

					Functions:
						add_adjacent_countries(self, adj_country_list, countries_object)
							Used in loading the dictionary, sets adjacent countries and determines amount of adjacent countries.
						update_available_colours(self, parent)
							Used to determine how many children should be made.
							Will check all neighbours that are already colored (and therefore in parent), and deletes their colors from available_colours list.

		benchmark:
		Functions needed to determine the performance of the algorithm.

			Functions:
				exportcsv(solution)
					Writes the array of numbers 'solution' to a csv file.
					This file can be used in Excel to create a histogram or other graph.

		importvis:
		Used to visualize either the map or network.
			
			Functions:
				Visualize(solution, my_map)
					Will create a map using matplotlib and numpy if a valid countryname is provided as my_map.
					If a networkname is provided, it will create a webbased visualization of the network.\

		algorithmv1:
		First algorithm. Simple depth first with some pruning (as described in report and presentation).

		algorithmv2:
		Second algorithm. Version 1 extended with single-color priority (see report and presentation).

		algorithmv3:
		Third algorithm. Version 2 extended with ordering by connections (again, see report/presentation).

		algorithmv4:
		Last and final algorithm. Selects the minimal chromatic number (report/presentation for details). 

		running_environment:
		USE THIS FILE TO TEST THE ALGORITHMS. Select graph to be used, algorithm version, and choose visualization or testing. 

