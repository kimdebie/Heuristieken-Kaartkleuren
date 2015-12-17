def Visualize(solution, my_map):

    if my_map in ['india', 'spain', 'USA']:

        # is used to display the map
        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        from matplotlib.collections import PatchCollection
        from matplotlib.patches import Polygon, PathPatch
        import matplotlib.animation as animation

        # get spain map working correctly with non english letters.
        import unicodedata

        # initiate the dict to use outside the function
        spain_dict = dict()

        def what_map_to_use(my_map):
        	# check what map is used!
        	if my_map == "india":
        		# ll means lowerleft, Northing and Easting, samen for Upper Right(UR)
        		# as projection we're using mercator, the coordinate sytem used by the shapefiles.
        		map = Basemap(llcrnrlon=69,llcrnrlat=23,urcrnrlon=79,urcrnrlat=30.3,
        		             resolution='i', projection='merc')

        		# read the geo shapefile.
        		map.readshapefile('JSON_files/Fixed_raj/IND_adm2', 'mkaart')
        		return map

        	elif my_map == 'spain':

        		# compensate for the incorrect names on the spain map given by heuristieken.nl
        		spain_dict.update({"jaen" : "lugo", "leon" : "a coruna","zamora" : "pontevedra","burgos" : "ourense","murcia" : "leon","guipuzcoa" : "asturias","toledo" : "zamora","pontevedra" : "salamanca","barcelona" : "caceres","madrid" : "badajoz","almeria" : "huelva","caceres" : "cadiz" ,"islas baleares" : "sevilla","albacete" : "malaga","las palmas" : "cordoba","valencia" : "ciudad real","cadiz" : "toledo","ciudad real" : "avila" ,"cantabria" : "valladolid","valladolid" : "palencia","guadalajara" :"cantabria","asturias" : "burgos","lugo": "segovia","huesca" : "la rioja","huelva" : "madrid","santa cruz de tenerife" : "jaen","zaragoza" : "granada","badajoz" : "soria","granada" : "guadalajara","sevilla" : "cuenca","vizcaya" : "albacete","cordoba" : "murcia","castellon" : "almeria","alava" : "alicante", "gerona" : "valencia","a coruna" : "teruel","salamanca" : "castellon","ourense" : "tarragona","alicante" : "zaragoza","navarra" : "navarra","segovia" : "alava","teruel" : "vizcaya","soria" : "guipuzcoa","malaga" : "huesca","tarragona" : "lleida","lleida" : "barcelona" ,"la rioja" : "girona"})

        		map = Basemap(llcrnrlon=-10,llcrnrlat=35.2,urcrnrlon=4.3,urcrnrlat=44,
        		             resolution='i', projection='merc')

        		map.readshapefile('JSON_files/Fixed_spaj/ESP_adm2', 'mkaart')
        		return map

        	elif my_map == 'USA':

        		map = Basemap(llcrnrlon=-82,llcrnrlat=39,urcrnrlon=-74,urcrnrlat=42.5,
        		             resolution='i', projection='merc')

        		map.readshapefile('JSON_files/Fixed_penns/USA_adm2', 'mkaart')
        		return map
        	# no need for else, because it is already checked at the create dictionary part.


        # -------------------- part to do the displaying of the results ---------------------- #

        # make the space to add the visualisation to.
        figure = plt.figure()

        # add a subplot 1 at position 1,1.
        ax = figure.add_subplot(111)

        # get shapefile
        mkaart = what_map_to_use(my_map)

        color_decoder = {"red" : "#a6cee3", "green" : "#1f78b4","yellow": "#b2df8a","blue" : "#33a02c", "purple" : "#fb9a99","pink" : "#e31a1c","orange" : "#fdbf6f" }


        # make empty array for the colored polygons.
        patches = []

        # empty the axis and remove them
        ax.clear()
        plt.axis('off')

            # add the color
            # if spain is not empty
        if my_map == 'spain':
            for key in spain_dict:
                for info, shape in zip(mkaart.mkaart_info, mkaart.mkaart):
                    uni_string = unicode(info["NAME_2"],'utf8')
                    uni_string = unicodedata.normalize('NFKD', uni_string ).encode('ascii', 'ignore')
                    if uni_string.lower().find(spain_dict[key]) != -1:
                        for entry in solution:
                            if entry.country_name == key:
                                color = color_decoder[entry.current_colour]

                        patches.append(Polygon(np.array(shape), True))
                        ax.add_collection(PatchCollection(patches, facecolor=  color, edgecolor='white', linewidths=1., zorder=2))
                        patches = []

        else:
            for key in solution:
                for info, shape in zip(mkaart.mkaart_info, mkaart.mkaart):
                    if info["NAME_2"].lower().find(key.country_name) != -1:
                        color = color_decoder[key.current_colour]
                        patches.append(Polygon(np.array(shape), True))
                        ax.add_collection(PatchCollection(patches, facecolor= color, edgecolor='white', linewidths=1., zorder=2))
                        patches = []
        # show the animation
        plt.show()

    elif my_map in ['network1', 'network2', 'network3', 'network4']:

        import csv

        with open('Network_files/solutionfile.csv', 'wb') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(["connection", "color"])
            for connection in solution:
                row = [connection.country_name, connection.current_colour]
                writer.writerow(row)

        import os
        location = os.path.dirname(os.path.realpath(__file__))
        print "Opening a server. Please remember to close the server after you're done."
        os.startfile(location + "/Network_files/visualization.bat")


        import webbrowser
        new = 2

        url = "http://localhost:8000/d3" + my_map + ".html"
        webbrowser.open(url,new=new)
