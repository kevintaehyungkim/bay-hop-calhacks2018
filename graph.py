from collections import defaultdict
from heapq import *
from bart_api import*
from google_maps_api import*
from uber_api import*
from lyft_api import *

import time
import numpy

# travel_means index - WALK, BIKE, CAR, UBER, LYFT, BART
def generate_min_travel_times(current_epoch_time, all_coordinates, travel_means):
	station_abbr_arr = []

	if len(all_coordinates) > 2:
		for i in range (1,len(all_coordinates)-1):
			station_abbr_arr.append(get_nearest_station(float(all_coordinates[i][0]), float(all_coordinates[i][1]))[1])

		bart_coordinates = all_coordinates[1:-1]
		# print(all_coordinates)
		# print(station_abbr_arr)

		bart_coordinate_dict = {}

		for i in range(0,len(bart_coordinates)-1):
			for j in range (i+1, len(bart_coordinates)):
				bart_pair_str = station_abbr_arr[i] + " " + station_abbr_arr[j]
				bart_coordinate_dict[bart_pair_str] = [bart_coordinates[i], bart_coordinates[j]]

		min_travel_time_dict = {}


		first_bart_station_departure_times = get_bart_travel_time(current_epoch_time, station_abbr_arr[0], station_abbr_arr[1])

		walk_time_to_first_bart = parseEpoch(walk_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])
		bike_time_to_first_bart = float("inf")
		car_time_to_first_bart = float("inf")
		uber_time_to_first_bart = float("inf")
		lyft_time_to_first_bart = float("inf")



		if travel_means[1]:
			bike_time_to_first_bart = parseEpoch(bike_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])

		if travel_means[2]:
			car_time_to_first_bart = parseEpoch(car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])

		if travel_means[3]:
			uber_time_to_first_bart = get_uber_travel_time(all_coordinates[0][0], all_coordinates[0][1], bart_coordinates[0][0], bart_coordinates[0][1])[1]

		if travel_means[4]:
			lyft = get_lyft_pickup_time(all_coordinates[0][0], all_coordinates[0][1])[1] + parseEpoch(car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])

		first_bart_time = float("inf")

		print(walk_time_to_first_bart)
		print(bike_time_to_first_bart)
		print(car_time_to_first_bart)
		print(uber_time_to_first_bart)
		print(lyft_time_to_first_bart)

		min_travel_time = min([walk_time_to_first_bart, bike_time_to_first_bart, car_time_to_first_bart, uber_time_to_first_bart, lyft_time_to_first_bart])

		for f in first_bart_station_departure_times:
			if current_epoch_time + min_travel_time <= f[0]:
				first_bart_time = f[0]
				break

		if min_travel_time == walk_time_to_first_bart:
			min_travel_time_dict['S'] = [f[0] - current_epoch_time, 'W']
		elif min_travel_time == bike_time_to_first_bart:
			min_travel_time_dict['S'] = [f[0] - current_epoch_time, 'BK']
		elif min_travel_time == car_time_to_first_bart:
			min_travel_time_dict['S'] = [f[0] - current_epoch_time, 'C']
		elif min_travel_time == uber_time_to_first_bart:
			min_travel_time_dict['S'] = [f[0] - current_epoch_time, 'U']
		elif min_travel_time == lyft_time_to_first_bart:
			min_travel_time_dict['S'] = [f[0] - current_epoch_time, 'L']


		for key in bart_coordinate_dict.keys():
			bart_coordinate_pairs = bart_coordinate_dict[key]
			car_time = parseEpoch(car_travel_time([[bart_coordinate_pairs[0][0], bart_coordinate_pairs[0][1]]], [[bart_coordinate_pairs[1][0], bart_coordinate_pairs[1][1]]])[0])
			bart_time_arr = get_bart_travel_time(first_bart_time, key.split()[0], key.split()[1])

			bart_time = bart_time_arr[0][1] - bart_time_arr[0][0]

			min_travel_time = min(bart_time, car_time)

			if min_travel_time == bart_time:
				min_travel_time_dict[key] = [min_travel_time, 'B']
			else:
				min_travel_time_dict[key] = [min_travel_time, 'C']

		print (min_travel_time_dict)
		return min_travel_time_dict


			# print(bart_time)
			# get_bart_travel_time(current_epoch_time, start_station_abbr, end_station_abbr):




	# nodes = []

	# start_node = Node(all_coordinates[0][0], all_coordinates[0][1], current_epoch_time, 'S')
	# end_node = Node(all_coordinates[len(all_coordinates)-1][0], all_coordinates[len(all_coordinates)-1][1], -1, 'E')

	# nodes.append(start_node)

	# # station_arrival_times = get_arrival_times(current_epoch_time, station_abbr_arr)
	
	# for i in range(0,len(station_arrival_times)):
	# 	for j in range(0,len(station_arrival_times[i])):
	# 		bart_station_node = Node(float(all_coordinates[j+1][0]), float(all_coordinates[j+1][1]), station_arrival_times[i][j], 'B')
	# 		nodes.append(bart_station_node)

	# nodes.append(end_node)

	# return nodes


# travel_means index - WALK, BIKE, CAR, UBER, LYFT, BART
# def generate_edges(nodes, travel_means):
# 	edges = []

# 	has_driven = False
# 	has_biked = False

# 	for i in range(0,len(nodes)-1):
# 		for j in range(i+1, len(nodes)):
# 			edge_array = [float("inf")] * 6
# 			bart_time = nodes[j].arrival_time - nodes[i].arrival_time 
# 			if travel_means[0]:
# 				walk = parseEpoch(walk_travel_time([[nodes[i].lat, nodes[i].lon]], [[nodes[j].lat, nodes[j].lon]])[0])
# 				if walk < bart_time:
# 					edge_array[0] = walk
# 			if travel_means[1]:
# 				bike = parseEpoch(bike_travel_time([[nodes[i].lat, nodes[i].lon]], [[nodes[j].lat, nodes[j].lon]])[0])
# 				if bike < bart_time:
# 					edge_array[1] = bike
# 			if travel_means[2]:
# 				car = parseEpoch(car_travel_time([[nodes[i].lat, nodes[i].lon]], [[nodes[j].lat, nodes[j].lon]])[0])


# 				# print(walk_travel_time([[37.8716, -122.258423]], [[37.7798, -122.4039]]))



# 				if car < bart_time:
# 					edge_array[2] = car
# 			if travel_means[3]:
# 				uber = get_uber_travel_time(nodes[i].lat, nodes[i].lon, nodes[j].lat, nodes[j].lon)[1]
# 				if uber < bart_time:
# 					edge_array[3] = uber
# 			if travel_means[4]:
# 				lyft = get_lyft_pickup_time(nodes[i].lat, nodes[i].lon)[1] + parseEpoch(car_travel_time([[nodes[i].lat, nodes[i].lon]], [[nodes[j].lat, nodes[j].lon]])[0])
# 				if lyft < bart_time:
# 					edge_array[4] = lyft
# 			if travel_means[5]:
# 				if bart_time >= 0:
# 					edge_array[5] = bart_time
# 			edges.append(edge_array)
# 	print(edges)
# 	return edges 


def parseEpoch(text):
	parts = text.split(' ')
	time = 0
	if len(parts) == 4:
		time += int(parts[0]) * 60 * 60
		time += int(parts[2]) * 60
	elif len(parts) == 2:
		time += int(parts[0]) * 60
	else:
		raise Exception('fuck')
	return time




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