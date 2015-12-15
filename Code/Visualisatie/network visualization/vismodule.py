def visualization(netnumber):
with open('solutionfile.csv', 'wb') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(["connection", "color"])
    for connection in solution:
        row = [connection.country_name, connection.current_colour]
        writer.writerow(row)

import webbrowser
new = 2


url = "file:" + ///C:/Users/Kim/Documents/GitHub/ + "Heuristieken-Kaartkleuren/Code/Visualisatie/network%20visualization/d3network" + netnumber + ".html"
webbrowser.open(url,new=new)