from collections import defaultdict
from multiprocessing import Manager, Pool
from heapq import *
from bart_api import*
from google_maps_api import*
from uber_api import*
from lyft_api import *

import time
import numpy
import multiprocessing as mp


CURRENT_DATE_TIME = 0
CURRENT_EPOCH_TIME = 0
MAX_BATCH_SIZE = 10
ROUTE_COORDS = []
NODES = []
INF = float("inf")

def lyft_travel_time_helper(a,b):
	return
	# print(get_lyft_pickup_time(b, c)[1])
	# d[a] = get_lyft_pickup_time(b, c)[1]


# travel_means index - WALK, BIKE, CAR, UBER, LYFT, BART
def generate_min_travel_times(current_epoch_time, all_coordinates, route_nodes, travel_means):

	# line_urls pool
	#uber wait time
	#lyft wait time
	# pool bart google maps

	global CURRENT_DATE_TIME
	global CURRENT_EPOCH_TIME
	global NODES
	global MAX_BATCH_SIZE

	CURRENT_DATE_TIME = time.localtime(current_epoch_time)
	CURRENT_EPOCH_TIME = current_epoch_time
	NODES = route_nodes

	bart_station_coordinates = all_coordinates[1:-1]

	lyft_coord_pairs = []
	# lyft_coord_pair_time_dict = manager.dict()


	# GOOGLE MAPS TRAVEL TIMES
	a = time.time()
	coord_keys = []
	car_coord_pair_time_dict = {}
	walk_coord_pair_time_dict = {}
	bike_coord_pair_time_dict = {}

	for i in range(0, len(all_coordinates)-1, MAX_BATCH_SIZE):
		origins_batch = all_coordinates[i:i+MAX_BATCH_SIZE]
		for j in range(i+1, len(all_coordinates), MAX_BATCH_SIZE):
			dest_batch = all_coordinates[j:j+MAX_BATCH_SIZE]
			for origin in origins_batch:
				for dest in dest_batch:
					coord_pair = str(origin) + ' ' + str(dest)
					coord_keys.append(coord_pair)

	travel_modes = []
	if travel_means[0]:
		travel_modes.append(0)
	if travel_means[1]:
		travel_modes.append(1)
	if travel_means[2] or travel_means[3] or travel_means[4]:
		travel_modes.append(2)

	travel_durations = travel_time(travel_modes, all_coordinates)

	for i in range(len(coord_keys)):
		if travel_means[0]:
			walk_coord_pair_time_dict[coord_keys[i]] = travel_durations['walking'][i]
		if travel_means[1]:
			bike_coord_pair_time_dict[coord_keys[i]] = travel_durations['bicycling'][i]
		if travel_means[2] or travel_means[3] or travel_means[4]:
			car_coord_pair_time_dict[coord_keys[i]] = travel_durations['driving'][i]

	# print(bike_coord_pair_time_dict)
	# print(car_coord_pair_time_dict)
	# print(walk_coord_pair_time_dict)
	b = time.time()
	print("Google Maps API: ", b-a)


	# LYFT WAIT TIME 
	# LYFT IN PROGRESS

	# a = time.time()
	# if travel_means[4]:
	# 	for i in range(0,len(all_coordinates)-1):
	# 		lyft_coord_str = str(all_coordinates[i][0]) + ' ' + str(all_coordinates[i][1])
	# 		lyft_coord_pairs.append([lyft_coord_str, all_coordinates[i][0], all_coordinates[i][1]])

	# 	for i in rangeg(0,len(lyft_coord_pairs)):


	# b = time.time()
	# print(lyft_coord_pair_time_dict)
	# print("Lyft: ", b-a)


	# BART TRAVEL TIME
	a = time.time()
	if travel_means[5]:
		bart_start = []
		bart_end = []
		for i in range(1,len(NODES)-2):
			for j in range(i+1, len(NODES)-1):
				bart_start.append(NODES[i])
				bart_end.append(NODES[j])
				
		bart_travel_time = get_bart_travel_time(CURRENT_DATE_TIME, CURRENT_EPOCH_TIME, bart_start, bart_end)

	b = time.time()
	print("BART: ", b-a)

	if len(all_coordinates) > 3:

		bart_coordinate_dict = {}

		for i in range(1,len(all_coordinates)-2):
			for j in range (i+1, len(all_coordinates)-1):
				bart_pair_str = NODES[i] + " " + NODES[j]
				bart_coordinate_dict[bart_pair_str] = [all_coordinates[i], all_coordinates[j]]

		min_travel_time_dict = {}

		first_bart_station_departure_times = []

		walk_time_to_first_bart = walk_coord_pair_time_dict[str(all_coordinates[0]) + ' ' + str(all_coordinates[1])]
		bike_time_to_first_bart = INF
		car_time_to_first_bart = INF
		uber_time_to_first_bart = INF
		lyft_time_to_first_bart = INF

		if travel_means[5]:
			first_bart_station_departure_times = bart_travel_time[NODES[1] + ' ' + NODES[2]]

		if travel_means[2]:
			car_time_to_first_bart = car_coord_pair_time_dict[str(all_coordinates[0]) + ' ' + str(all_coordinates[1])]

		if travel_means[1]:
			bike_time_to_first_bart = bike_coord_pair_time_dict[str(all_coordinates[0]) + ' ' + str(all_coordinates[1])]

		if travel_means[3]:
			uber_time_to_first_bart = 180 + car_coord_pair_time_dict[str(all_coordinates[0]) + ' ' + str(all_coordinates[1])]

		if travel_means[4]:
			# print(str(all_coordinates[0][0]) + ' ' + str(all_coordinates[0][1]))
			lyft_time_to_first_bart = lyft_coord_pair_time_dict[str(all_coordinates[0][0]) + ' ' + str(all_coordinates[0][1])] + car_time_to_first_bart

		first_bart_time = INF


		min_travel_time = min([walk_time_to_first_bart, bike_time_to_first_bart, car_time_to_first_bart, uber_time_to_first_bart, lyft_time_to_first_bart])

		if travel_means[5]:
			for f in first_bart_station_departure_times:
				if current_epoch_time + min_travel_time < f[0]:
					first_bart_time = f[0]

				if min_travel_time == walk_time_to_first_bart:
					min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'W']
				elif min_travel_time == bike_time_to_first_bart:
					min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'BK']
				elif min_travel_time == car_time_to_first_bart:
					min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'C']
				elif min_travel_time == uber_time_to_first_bart:
					min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'U']
				elif min_travel_time == lyft_time_to_first_bart:
					min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'L']
				break
		else:
			if min_travel_time == walk_time_to_first_bart:
				min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'W']
			elif min_travel_time == bike_time_to_first_bart:
				min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'BK']
			elif min_travel_time == car_time_to_first_bart:
				min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'C']
			elif min_travel_time == uber_time_to_first_bart:
				min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'U']
			elif min_travel_time == lyft_time_to_first_bart:
				min_travel_time_dict['S ' + NODES[1]] = [min_travel_time, 'L']


		for key in bart_coordinate_dict.keys():
			bart_coordinate_pairs = bart_coordinate_dict[key]
			
			car_time = INF
			uber_time = INF
			lyft_time = INF
			bart_time_diff = INF

			if travel_means[2]:
				car_time = car_coord_pair_time_dict[str(bart_coordinate_pairs[0]) + ' ' + str(bart_coordinate_pairs[1])]
			if travel_means[3]:
				uber_time = car_coord_pair_time_dict[str(bart_coordinate_pairs[0]) + ' ' + str(bart_coordinate_pairs[1])] + 180
			if travel_means[4]:
				lyft_time = lyft_coord_pair_time_dict[str(bart_coordinate_pairs[0][0]) + ' ' + str(bart_coordinate_pairs[0][1])] + car_coord_pair_time_dict[str(bart_coordinate_pairs[0][0]) + ' ' + str(bart_coordinate_pairs[0][1])]

			if travel_means[5]:
				bart_time_arr = bart_travel_time[key.split()[0] + ' ' + key.split()[1]]
				bart_time_diff = bart_time_arr[0][1] - bart_time_arr[0][0]

			min_travel_time = min(bart_time_diff, uber_time, lyft_time)

			if min_travel_time == bart_time_diff:
				min_travel_time_dict[key] = [min_travel_time, 'B']
			elif min_travel_time == uber_time:
				min_travel_time_dict[key] = [min_travel_time, 'U']
			else:
				min_travel_time_dict[key] = [min_travel_time, 'L']


		start_coordinate = all_coordinates[0]
		end_coordinate = all_coordinates[len(all_coordinates)-1]


		for i in range (1,len(all_coordinates)):
			next_coordinate = all_coordinates[i]

			# from start to all upcoming series of coordinates
			walk_time_from_start = walk_coord_pair_time_dict[str(start_coordinate) + ' ' + str(next_coordinate)]
			bike_time_from_start = INF
			car_time_from_start = INF
			uber_time_from_start = INF
			lyft_time_from_start = INF

			if travel_means[1]:
				bike_time_from_start = bike_coord_pair_time_dict[str(start_coordinate) + ' ' + str(next_coordinate)]

			if travel_means[2]:
				car_time_from_start = car_coord_pair_time_dict[str(start_coordinate) + ' ' + str(next_coordinate)]

			if travel_means[3]:
				uber_time_from_start = 180 + car_coord_pair_time_dict[str(start_coordinate) + ' ' + str(next_coordinate)]

			if travel_means[4]:
				lyft_time_from_start = lyft_coord_pair_time_dict[str(start_coordinate[0]) + ' ' + str(start_coordinate[1])] + car_coord_pair_time_dict[str(start_coordinate) + ' ' + str(next_coordinate)]

			min_travel_time = min([walk_time_from_start, bike_time_from_start, car_time_from_start, uber_time_from_start, lyft_time_from_start])

			key_pair = 'S ' + NODES[i]


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

				walk_time_to_end = walk_coord_pair_time_dict[str(next_coordinate) + ' ' + str(end_coordinate)]
				bike_time_to_end = INF
				uber_time_to_end = INF
				lyft_time_to_end = INF
				car_time_to_end = INF

				if travel_means[1]:
					bike_time_to_end = bike_coord_pair_time_dict[str(next_coordinate) + ' ' + str(end_coordinate)]

				if travel_means[3]:
					uber_time_to_end = 180 + car_time_to_end

				if travel_means[4]:
					lyft_time_to_end = lyft_coord_pair_time_dict[str(next_coordinate[0]) + ' ' + str(next_coordinate[1])] + car_time_to_end

				min_travel_time = min([walk_time_to_end, bike_time_to_end, uber_time_to_end, lyft_time_to_end])

				key_pair = NODES[i] + ' E'

				if min_travel_time == walk_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'W']
				elif min_travel_time == bike_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'BK']
				elif min_travel_time == uber_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'U']
				elif min_travel_time == lyft_time_to_end:
					min_travel_time_dict[key_pair] = [min_travel_time, 'L']

	else:
		walk_time = walk_coord_pair_time_dict[str(all_coordinates) + ' ' + str(all_coordinates)]

		if travel_means[2]:
			car_time = car_coord_pair_time_dict[str(all_coordinates) + ' ' + str(all_coordinates)]

		if travel_means[1]:
			bike_time = bike_coord_pair_time_dict[str(all_coordinates) + ' ' + str(all_coordinates)]

		if travel_means[3]:
			uber_time = 3 + car_time

		if travel_means[4]:
			# print(str(all_coordinates[0][0]) + ' ' + str(all_coordinates[0][1]))
			lyft_time_to_first_bart = lyft_coord_pair_time_dict[str(all_coordinates[0][0]) + ' ' + str(all_coordinates[0][1])] + car_time

		min_travel_time = min([walk_time, bike_time, car_time, uber_time, lyft_time])

		key_pair = NODES[0] + ' ' + NODES[2]

		if min_travel_time == car_time:
			min_travel_time_dict[key_pair] = [min_travel_time, 'C']
		elif min_travel_time == bike_time:
			min_travel_time_dict[key_pair] = [min_travel_time, 'BK']
		elif min_travel_time == uber_time:
			min_travel_time_dict[key_pair] = [min_travel_time, 'U']
		elif min_travel_time == lyft_time:
			min_travel_time_dict[key_pair] = [min_travel_time, 'L']
		elif min_travel_time == walk_time:
			min_travel_time_dict[key_pair] = [min_travel_time, 'W']


	print (min_travel_time_dict)
	return min_travel_time_dict



# solve dp problem given most optimal edges in dictionary_weights
# path stores best travel time to get to node i
# trans stores a list of tuples [( (node1, node2) , means)]
def dp_reader(dictionary_weights, zzz):
	global NODES


	# print(dictionary_weights)
	# for i in range(len(NODES)):
	# 	NODES[i] = 

	path = numpy.zeros(len(NODES))
	trans = [[] for i in range(len(NODES))]
	trans[0] = []
	path[1] = get_time(dictionary_weights, "S", NODES[1])
	temp = ["S " + NODES[1], get_means(dictionary_weights, "S", NODES[1])]
	trans[1] = [temp]
	for i in range(2,len(NODES)):
		minCost = INF
		minMethod = []
		curr = NODES[i]
		for j in range(0,i):
			prev = NODES[j]
			temp_path = get_time(dictionary_weights, prev, curr) + path[j]
			if temp_path < minCost:
				minCost = temp_path
				minMethod = trans[j].copy()
				minMethod.append([prev + " " + curr, get_means(dictionary_weights, prev, curr)])
				
		path[i] = minCost
		trans[i] = minMethod

	return [path[-1], trans[-1]]



# def dp_reader(dictionary_weights, zzz):
#  	nodes = []
# 	for z in zzz:
# 	nodes.append(Node('S'))
#  	for i in range(1,len(zzz)-1):
# 		z = zzz[i]
# 		station_abbr = get_nearest_station(float(z[0]), float(z[1]))[1]
# 		nodes.append(Node(station_abbr))
#  	nodes.append(Node('E'))
#  	path = numpy.zeros(len(nodes))
# 	trans = [[] for i in range(len(nodes))]
#  	path[1] = get_time(dictionary_weights, "S", nodes[1].name)
#  	trans[0] = []
# 	path[1] = get_time(dictionary_weights, "S", nodes[1].name)
# 	temp = ("S " + nodes[1].name, get_means(dictionary_weights, "S", nodes[1].name))
# 	trans[1] = [temp]
# 	for i in range(2,len(nodes)):
#  		minCost = float("inf")
# 		minMethod = []
# 		curr = nodes[i].name
# @@ -202,48 +290,20 @@ def dp_reader(dictionary_weights, zzz):
# 				minCost = temp_path
# 				minMethod = trans[j].copy()
# 				minMethod.append((prev + " " + curr, get_means(dictionary_weights, prev, curr)))
				
# 		path[i] = minCost
# 		trans[i] = minMethod
#  	return path[-1], trans[-1]






def get_time(dictionary_weights, start, end):
	value = dictionary_weights[start + " " + end]
	return value[0]

def get_means(dictionary_weights, start, end):
	value = dictionary_weights[start + " " + end]
	return value[1]


# Class Node
# includes name of node as a string
# "S" - Start, "DBRK" - Abbreviation of BART station, "E" - End
class Node:
	def __init__(self, name, duration):
		self.name = name
		self.duration = duration
		self.price = price




# This function returns the lowest weight between two nodes among the
# potential modes of transportation.
# Arguments:
#   origins, destinations: start and end location node arrays
#   tm: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type integer]
#   weight of edge in seconds