from collections import defaultdict
from multiprocessing import Pool
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
NODES = []


def bart_travel_time_helper(a):
	global CURRENT_DATE_TIME
	global CURRENT_EPOCH_TIME

	a[0][a[1]] = get_bart_travel_time(CURRENT_DATE_TIME, CURRENT_EPOCH_TIME, a[2], a[3])

def lyft_travel_time_helper(a):
	a[0][a[1]] = get_lyft_pickup_time(a[2], a[3])[1]


# travel_means index - WALK, BIKE, CAR, UBER, LYFT, BART
def generate_min_travel_times(current_epoch_time, all_coordinates, travel_means):

	######
	######
	# TODO: 1 BART STATION (both close to same one)
	######
	######


	global CURRENT_DATE_TIME
	global CURRENT_EPOCH_TIME
	global NODES

	CURRENT_DATE_TIME = time.localtime(current_epoch_time)
	CURRENT_EPOCH_TIME = current_epoch_time

	station_abbr_arr = []

	bart_station_coordinates = all_coordinates[1:-1]
	bart_coord_pairs = []
	lyft_coord_pairs = []
	bart_coord_pair_time_dict = {}
	lyft_coord_pair_time_dict = {}

	# NODES - abbreviations of all nodes
	# S - Start, 'DBRK' - BART Station, E - End
	NODES.append('S')
	for i in range(1,len(all_coordinates)-1):
		coordinate = all_coordinates[i]
		station_abbr = get_nearest_station(float(coordinate[0]), float(coordinate[1]))[1]
		NODES.append(station_abbr)
	NODES.append('E')

	manager = mp.Manager()
	bart_travel_time = manager.dict()
	lyft_travel_time = manager.dict()

	# BART TRAVEL TIME
	if travel_means[5]:
		for i in range(0,len(bart_station_coordinates)-1):
			for j in range(i+1, len(bart_station_coordinates)):
				bart_coord_pair_str = NODES[i+1] + ' ' + NODES[j+1]
				bart_coord_pairs.append([bart_travel_time, bart_coord_pair_str, NODES[i+1], NODES[j+1]])
		pool = Pool(processes=12)  
		pool.map(bart_travel_time_helper, bart_coord_pairs)

	# LYFT WAIT TIME 
	if travel_means[4]:
		for i in range(0,len(all_coordinates)-1):
			lyft_coord_pair_str = str(all_coordinates[i][0]) + ' ' + str(all_coordinates[i][1])
			lyft_coord_pairs.append([lyft_travel_time, lyft_coord_pair_str, all_coordinates[i][0], all_coordinates[i][1]])

		pool = Pool(processes=64)
		pool.map(lyft_travel_time_helper, lyft_coord_pairs)



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

		first_bart_station_departure_times = bart_travel_time[NODES[1] + ' ' + NODES[2]]

		walk_time_to_first_bart = walk_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0]
		bike_time_to_first_bart = float("inf")
		car_time_to_first_bart = float("inf")
		uber_time_to_first_bart = float("inf")
		lyft_time_to_first_bart = float("inf")

		car_time = car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0]

		if travel_means[1]:
			bike_time_to_first_bart = bike_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[bart_coordinates[0][0], bart_coordinates[0][1]]])[0]

		if travel_means[2]:
			car_time_to_first_bart = car_time

		if travel_means[3]:
			uber_time_to_first_bart = 5 + car_time

		if travel_means[4]:
			lyft_time_to_first_bart = lyft_travel_time['' + str(all_coordinates[0][0]) + ' ' + str(all_coordinates[0][1])] + car_time

		first_bart_time = float("inf")


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

		# keep values of wait time for each app
		# key:value -> abbr:wait time
		uber_wait_times = {}
		lyft_wait_times = {}
		seen_stations = set()


		for key in bart_coordinate_dict.keys():
			bart_coordinate_pairs = bart_coordinate_dict[key]
			car_time = car_travel_time([[bart_coordinate_pairs[0][0], bart_coordinate_pairs[0][1]]], [[bart_coordinate_pairs[1][0], bart_coordinate_pairs[1][1]]])[0]
		
			uber_time = float("inf")
			lyft_time = float("inf")

			if travel_means[3]:
				uber_time = car_time + 5
			if travel_means[4]:

				azaaas = str(bart_coordinate_pairs[0][0]) + ' ' + str(bart_coordinate_pairs[0][1])
				lyft_time = lyft_travel_time[azaaas] + car_time

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
			walk_time_from_start = walk_travel_time([[start_coordinate[0], start_coordinate[1]]], [[next_coordinate[0], next_coordinate[1]]])[0]
			bike_time_from_start = float("inf")
			car_time_from_start = float("inf")
			uber_time_from_start = float("inf")
			lyft_time_from_start = float("inf")

			car_time = car_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[next_coordinate[0], next_coordinate[1]]])[0]

			if travel_means[1]:
				bike_time_from_start = bike_travel_time([[all_coordinates[0][0], all_coordinates[0][1]]], [[next_coordinate[0], next_coordinate[1]]])[0]

			if travel_means[2]:
				car_time_from_start = car_time

			if travel_means[3]:
				uber_time_from_start = 5 + car_time

			if travel_means[4]:
				lyft_time_from_start = lyft_travel_time[str(start_coordinate[0]) + ' ' + str(start_coordinate[1])] + car_time

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
				walk_time_to_end = walk_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0]
				bike_time_to_end = float("inf")
				uber_time_to_end = float("inf")
				lyft_time_to_end = float("inf")

				car_time = car_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0]

				if travel_means[1]:
					bike_time_to_end = bike_travel_time([[next_coordinate[0], next_coordinate[1]]], [[end_coordinate[0], end_coordinate[1]]])[0]

				if travel_means[3]:
					uber_time_to_end = 5 + car_time

				if travel_means[4]:
					lyft_time_to_end = lyft_travel_time[str(next_coordinate[0]) + ' ' + str(next_coordinate[1])] + car_time


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

	print (min_travel_time_dict)
	return min_travel_time_dict



# solve dp problem given most optimal edges in dictionary_weights
# path stores best travel time to get to node i
# trans stores a list of tuples [( (node1, node2) , means)]
def dp_reader(dictionary_weights, zzz):
	global NODES



	path = numpy.zeros(len(NODES))
	trans = [[] for i in range(len(NODES))]
	trans[0] = []
	path[1] = get_time(dictionary_weights, "S", NODES[1])
	temp = ("S " + NODES[1], get_means(dictionary_weights, "S", NODES[1]))
	trans[1] = [temp]
	for i in range(2,len(NODES)):
		minCost = float("inf")
		minMethod = []
		curr = NODES[i]
		for j in range(0,i):
			prev = NODES[j]
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


# Class Node
# includes name of node as a string
# "S" - Start, "DBRK" - Abbreviation of BART station, "E" - End
class Node:
	def __init__(self, name):
		self.name = name




# This function returns the lowest weight between two nodes among the
# potential modes of transportation.
# Arguments:
#   origins, destinations: start and end location node arrays
#   tm: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type integer]
#   weight of edge in seconds