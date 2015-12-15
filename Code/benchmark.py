'''
exporting a csv file of a certain number of runs of the coloring algorithm
'''

import csv

def exportcsv(solution):
	csvfile = open("output.csv", 'wb');

	csvwriter = csv.writer(csvfile, delimiter=',')

	for number in solution:
		csvwriter.writerow([number])