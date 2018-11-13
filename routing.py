# Base-URL: http://localhost:5000/

from flask import Flask
from flask import Markup
from flask import Flask, flash, redirect, url_for, request, render_template, json, session, abort

from uber_api import get_uber_travel_time
from lyft_api import *
from bart_api import get_nearest_station, get_bart_travel_time, get_stations_between, get_station_coordinates
from graph import *

import time

CURRENT_TIME = 0
START_COORDINATES = []
END_COORDINATES = []

config_parser = SafeConfigParser()
config_parser.read('station_names.cfg')


# Provides the quickest routes from current location to destination using provided travel means
# INDEX: WALK, BIKE, CAR, UBER, LYFT, BART
# Inputs -
	# current: current address
	# destination: destination address
	# travel_means: array of travel methods selected by the user (excludes walking which is defaulted)
#
def generate_graph(current, destination, travel_means):

	a = time.time()

	route_coords = []
	route_nodes = []
	means_of_transportation = [1] + travel_means

	CURRENT_TIME = time.time()
	START_COORDINATE = current
	END_COORDINATE = destination

	route_coords.append(START_COORDINATE)
	start_end_station = get_nearest_station([[START_COORDINATE[0], START_COORDINATE[1]], [END_COORDINATE[0], END_COORDINATE[1]]])
	start_station = start_end_station[0][1]
	end_station = start_end_station[1][1]
	stations_between = get_stations_between(start_station, end_station)
	route_nodes = ['S'] + stations_between + ['E']
	station_coordinates = get_station_coordinates(stations_between)

	for station_coordinate in station_coordinates:
		route_coords.append([float(station_coordinate[0]), float(station_coordinate[1])])

	route_coords.append(END_COORDINATE)

	b = time.time()
	print("pre-API: ", b-a)

	min_travel_times = generate_min_travel_times(
		CURRENT_TIME, 
		route_coords, 
		route_nodes, 
		means_of_transportation)

	return process_graph(dp_reader(min_travel_times, route_coords))


# Process route nodes 
def process_graph(route_nodes):

	trip_info = []
	# processed_route = []
	total_duration = route_nodes[0]
	processed_route = route_nodes[1]

	hours = int(total_duration // 3600)
	total_duration %= 3600
	minutes = int(total_duration // 60)
	trip_info.append([hours, minutes])

	# TODO: up to 3 or more ....
	# for i in range(0,len(route)):
	# 	current_node = route[i]
	# 	next_node = route[i]
	# 	if current_node[2] == next_node[2]:

	# TODO: BART Station instead of abbreviation
	if len(processed_route) > 2:
		for i in range(len(processed_route)):
			node_pair = processed_route[i][0].split()
			if i == 0:
				processed_route[i] = ['S', config_parser.get(node_pair[1],'name'), processed_route[i][1]]
			elif i == len(processed_route)-1:
				processed_route[i] = [config_parser.get(node_pair[0],'name'), 'E', processed_route[i][1]]
			else:
				processed_route[i] = [config_parser.get(node_pair[0],'name'), config_parser.get(node_pair[1],'name'), processed_route[i][1]]
	else:
		processed_route[0] = ['S', 'E', processed_route[0][1]]

	trip_info.append(processed_route)


	print(trip_info)
	return trip_info


	# [3440.0, [['S DBRK', 'W'], ['DBRK POWL', 'B'], ['POWL E', 'W']]]


# a = time.time()
# generate_graph([37.7798, -122.4039], [37.8638745,-122.2593799],[1,0,0,0,1])
# b=time.time()
# print("Total: ", b-a, "seconds")


