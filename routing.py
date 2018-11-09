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

# INDEX: WALK, BIKE, CAR, UBER, LYFT, BART
MEANS_OF_TRANSPORATION = [1]
ROUTE_COORDS = []
ROUTE_NODES = []

# Provides the quickest routes from current location to destination using provided travel means
# Inputs -
	# current: current address
	# destination: destination address
	# travel_means: array of travel methods selected by the user
def generate_graph(current, destination, travel_means):

	a = time.time()

	global CURRENT_TIME
	global START_COORDINATE
	global END_COORDINATE
	global ROUTE_COORDS
	global MEANS_OF_TRANSPORATION

	CURRENT_TIME = time.time()
	MEANS_OF_TRANSPORATION += travel_means
	START_COORDINATE = current
	END_COORDINATE = destination

	ROUTE_COORDS.append(START_COORDINATE)
	start_end_station = get_nearest_station([[START_COORDINATE[0], START_COORDINATE[1]], [END_COORDINATE[0], END_COORDINATE[1]]])
	start_station = start_end_station[0][1]
	end_station = start_end_station[1][1]
	stations_between = get_stations_between(start_station, end_station)
	ROUTE_NODES = ['S'] + stations_between + ['E']
	station_coordinates = get_station_coordinates(stations_between)

	for station_coordinate in station_coordinates:
		ROUTE_COORDS.append([float(station_coordinate[0]), float(station_coordinate[1])])

	ROUTE_COORDS.append(END_COORDINATE)

	b = time.time()
	print("pre-API: ", b-a)

	min_travel_times = generate_min_travel_times(CURRENT_TIME, ROUTE_COORDS, ROUTE_NODES, MEANS_OF_TRANSPORATION)

	return process_graph(dp_reader(min_travel_times, ROUTE_COORDS))


# Process directed graph to find the quickest route to destination
def process_graph(route_nodes):
	for r in route_nodes:
		print(r)
	return route_nodes


a = time.time()
generate_graph([37.8694, -122.2719], [37.7798, -122.4039],[1,1,0,0,1])
b=time.time()
print("Total: ", b-a, "seconds")

# MLK
# 37.8694° N, 122.2719


# print(calculate_route([37.880082, -122.274871], [37.879170, -122.269055],[1,1,0,0,0,1]))

# print(generate_nodes([37.7798, -122.403], [37.8716, -122.258423]))


