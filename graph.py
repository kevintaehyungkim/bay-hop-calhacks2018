from collections import defaultdict
from heapq import *
from bart_api import*
from google_maps_api import*
from uber_api import*
from lyft_api import *

import time
import numpy

# travel_means index - WALK, BIKE, CAR, UBER, LYFT, BART

#TODO: END STUFF, HAS DRIVEN STUFF FOR END

def generate_min_travel_times(current_epoch_time, all_coordinates, travel_means):
	station_abbr_arr = []

	if len(all_coordinates) > 2:
		for i in range (1,len(all_coordinates)-1):
			station_abbr_arr.append(get_nearest_station(float(all_coordinates[i][0]), float(all_coordinates[i][1]))[1])

		bart_coordinates = all_coordinates[1:-1]

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

		# print(bart_coordinates[0][0])
		# print(bart_coordinates[0][1])

		if travel_means[1]:
			bike_time_to_first_bart = parseEpoch(bike_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])

		if travel_means[2]:
			car_time_to_first_bart = parseEpoch(car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])

		if travel_means[3]:
			uber_time_to_first_bart = get_uber_travel_time(all_coordinates[0][0], all_coordinates[0][1], bart_coordinates[0][0], bart_coordinates[0][1])[1]

		if travel_means[4]:
			lyft_time_to_first_bart = get_lyft_pickup_time(all_coordinates[0][0], all_coordinates[0][1])[1] + parseEpoch(car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0])

		first_bart_time = float("inf")

		# print(walk_time_to_first_bart)
		# print(bike_time_to_first_bart)
		# print(car_time_to_first_bart)
		# print(uber_time_to_first_bart)
		# print(lyft_time_to_first_bart)

		min_travel_time = min([walk_time_to_first_bart, bike_time_to_first_bart, car_time_to_first_bart, uber_time_to_first_bart, lyft_time_to_first_bart])

		for f in first_bart_station_departure_times:
			if current_epoch_time + min_travel_time <= f[0]:
				first_bart_time = f[0]

			if min_travel_time == walk_time_to_first_bart:
				min_travel_time_dict['S POWL'] = [min_travel_time, 'W']
			elif min_travel_time == bike_time_to_first_bart:
				min_travel_time_dict['S POWL'] = [min_travel_time, 'BK']
			elif min_travel_time == car_time_to_first_bart:
				min_travel_time_dict['S POWL'] = [min_travel_time, 'C']
			elif min_travel_time == uber_time_to_first_bart:
				min_travel_time_dict['S POWL'] = [min_travel_time, 'U']
			elif min_travel_time == lyft_time_to_first_bart:
				min_travel_time_dict['S POWL'] = [min_travel_time, 'L']

			break


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

		start_coordinate = all_coordinates[0]
		end_coordinate = all_coordinates[len(all_coordinates)-1]

		abbreviations = []
		abbreviations.append('S')

		for i in range(1,len(all_coordinates)-1):
			coordinate = all_coordinates[i]
			station_abbr = get_nearest_station(float(coordinate[0]), float(coordinate[1]))[1]
			abbreviations.append(station_abbr)

		abbreviations.append('E')


		for i in range (1,len(all_coordinates)):

			next_coordinate = all_coordinates[i]

			# from start to all upcoming series of coordinates
			walk_time_from_start = parseEpoch(walk_travel_time([[start_coordinate[0], start_coordinate[1]]], [[next_coordinate[0], next_coordinate[1]]])[0])
			bike_time_from_start = float("inf")
			car_time_from_start = float("inf")
			uber_time_from_start = float("inf")
			lyft_time_from_start = float("inf")

			if travel_means[1]:
				bike_time_from_start = parseEpoch(bike_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[next_coordinate[0], next_coordinate[1]]])[0])

			if travel_means[2]:
				car_time_from_start = parseEpoch(car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[next_coordinate[0], next_coordinate[1]]])[0])

			if travel_means[3]:
				uber_time_from_start = get_uber_travel_time(start_coordinate[0], start_coordinate[1], next_coordinate[0], next_coordinate[1])[1]

			if travel_means[4]:
				lyft_time_from_start = get_lyft_pickup_time(start_coordinate[0], start_coordinate[1])[1] + parseEpoch(car_travel_time([[start_coordinate[0], start_coordinate[1]]], [[next_coordinate[0], next_coordinate[1]]])[0])

			min_travel_time = min([walk_time_from_start, bike_time_from_start, car_time_from_start, uber_time_from_start, lyft_time_from_start])

			key_pair = 'S ' + abbreviations[i]

			if min_travel_time == walk_time_from_start:
				min_travel_time_dict[key_pair] = [min_travel_time, 'W']
			elif min_travel_time == bike_time_from_start:
				min_travel_time_dict[key_pair] = [min_travel_time, 'BK']
			elif min_travel_time == car_time_from_start:
				min_travel_time_dict[key_pair] = [min_travel_time, 'C']
			elif min_travel_time == uber_time_from_start:
				min_travel_time_dict[key_pair] = [min_travel_time, 'U']
			elif min_travel_time == lyft_time_from_start:
				min_travel_time_dict[key_pair] = [min_travel_time, 'L']


			# from next coordinate to end
			if i < len(all_coordinates)-1:
				walk_time_to_end = parseEpoch(walk_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0])
				bike_time_to_end = float("inf")
				car_time_to_end = float("inf")
				uber_time_to_end = float("inf")
				lyft_time_to_end = float("inf")

				if travel_means[1]:
					bike_time_to_end = parseEpoch(bike_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0])

				if travel_means[2]:
					car_time_to_end = parseEpoch(car_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0])

				if travel_means[3]:
					uber_time_to_end = get_uber_travel_time(next_coordinate[0], next_coordinate[1], end_coordinate[0], end_coordinate[1])[1]

				if travel_means[4]:
					lyft_time_to_end = get_lyft_pickup_time(next_coordinate[0], next_coordinate[1])[1] + parseEpoch(car_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0])

				min_travel_time = min([walk_time_to_end, bike_time_to_end, car_time_to_end, uber_time_to_end, lyft_time_to_end])

				key_pair = abbreviations[i] + ' E'

				if min_travel_time == walk_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'W']
				elif min_travel_time == bike_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'BK']
				elif min_travel_time == car_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'C']
				elif min_travel_time == uber_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'U']
				elif min_travel_time == lyft_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'L']


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


# solve dp problem given most optimal edges in dictionary_weights
# path stores best travel time to get to node i
# trans stores a list of tuples [( (node1, node2) , means)]
def dp_reader(dictionary_weights, zzz):

	nodes = []
	nodes.append(Node('S'))

	for i in range(1,len(zzz)-1):
		z = zzz[i]
		station_abbr = get_nearest_station(float(z[0]), float(z[1]))[1]
		nodes.append(Node(station_abbr))

	nodes.append(Node('E'))

	path = numpy.zeros(len(nodes))
	trans = [[] for i in range(len(nodes))]
	trans[0] = []
	path[1] = get_time(dictionary_weights, "S", nodes[1].name)
	temp = ("S " + nodes[1].name, get_means(dictionary_weights, "S", nodes[1].name))
	trans[1] = [temp]
	for i in range(2,len(nodes)):
		minCost = float("inf")
		minMethod = []
		curr = nodes[i].name
		for j in range(0,i-1):
			prev = nodes[j].name
			temp_path = get_time(dictionary_weights, prev, curr) + path[j]
			if temp_path < minCost:
				minCost = temp_path
				minMethod = trans[j].copy()
				minMethod.append((prev + " " + curr, get_means(dictionary_weights, prev, curr)))
				
		path[i] = minCost
		trans[i] = minMethod

	return path[-1], trans[-1]

def get_time(dictionary_weights, start, end):
	value = dictionary_weights[start + " " + end]
	return value[0]

def get_means(dictionary_weights, start, end):
	value = dictionary_weights[start + " " + end]
	return value[1]

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

# Class Node
# includes name of node as a string
# "S" - Start, "DBRK" - Abbreviation of BART station, "E" - End
class Node:
	def __init__(self, name):
		self.name = name





# class Node:
#     def __init__(self, lat, lon, arrival_time, node_type):
#         self.lat = lat
#         self.lon = lon
#         self.station = get_nearest_station(lat, lon)
#         self.node_type = node_type
#         self.arrival_time = arrival_time #epoch
#         self.traveled = [0, 0, 0, 0, 0, 0]
#         self.transport_modes = [0, 0, 0, 0, 0, 0]



# This function returns the lowest weight between two nodes among the
# potential modes of transportation.
# Arguments:
#   origins, destinations: start and end location node arrays
#   tm: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type integer]
#   weight of edge in seconds