from collections import defaultdict
from heapq import *
from bart_api import*
from google_maps_api import*
from uber_api import*

import time
import numpy


def generate_graph(current_epoch_time, all_coordinates, travel_means):
	print(current_epoch_time)
	print(all_coordinates)
	print(travel_means)

	station_abbr_arr = []

	if len(all_coordinates) > 2:
		for i in range (1,len(all_coordinates)-1):
			station_abbr_arr.append(get_nearest_station(float(all_coordinates[i][0]), float(all_coordinates[i][1]))[1])

	station_arrival_times = [[123,124,125],[124,125,126]]

	nodes = []

	start_node = Node(all_coordinates[0][1], all_coordinates[0][1], current_epoch_time, 'S')
	nodes.append(start_node)


	print("!@#!@#!@#!@#!@#!@#")

	
	for i in range(0,len(station_arrival_times)):
		for j in range(0,len(station_arrival_times[i])):
			bart_station_node = Node(all_coordinates[i+1][0], all_coordinates[i+1][1], station_arrival_times[i][j], 'B')
			nodes.append(bart_station_node)

	print (nodes)


	# station_arrival_nodes = get_arrival_times(current_epoch_time, station_abbr_arr)

	return





class Node:
    def __init__(self, lat, lon, arrival_time, node_type):
        self.lat = lat
        self.lon = lon
        self.station = get_nearest_station(lat, lon)
        self.node_type = node_type
        self.arrival_time = arrival_time #epoch
        self.traveled = [0, 0, 0, 0, 0, 0]
        self.transport_modes = [0, 0, 0, 0, 0, 0]



# This function returns the lowest weight between two nodes among the
# potential modes of transportation.
# Arguments:
#   origins, destinations: start and end location node arrays
#   tm: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type integer]
#   weight of edge in seconds