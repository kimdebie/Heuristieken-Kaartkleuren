'''
exporting a csv file of a certain number of runs of the coloring algorithm
'''

import csv

def exportcsv(solution):
	csv = open("output.csv", 'w');

	csvwriter = csv.writer(csv)

	csvwriter.writerows(solution)