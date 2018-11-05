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
MEANS_OF_TRANSPORATION = [1,0,0,0,0,0]

ROUTE_NODES = []

# Provides the quickest routes from current location to destination using provided travel means
# Inputs -
	# current: current address
	# destination: destination address
	# travel_means: array of travel methods selected by the user
def calculate_route(current, destination, travel_means):
	CURRENT_TIME = time.time()
	# MEANS_OF_TRANSPORATION = travel_means
	# START_COORDINATES = #
	# END_COORDINATES = #

	#process_nodes
	return generate_graph(current, destination, travel_means)

# Generates nodes based on start and end coordinates provided
def generate_graph(START_COORDINATES, END_COORDINATES, TRAVEL_MEANS): 
	# starting location (first node)
	ROUTE_NODES.append(START_COORDINATES)
	# if no need to take bart, add that in later 
	start_station = get_nearest_station(START_COORDINATES[0], START_COORDINATES[1])
	end_station = get_nearest_station(END_COORDINATES[0], END_COORDINATES[1])
	stations_between = get_stations_between(start_station[1], end_station[1])
	station_coordinates = get_station_coordinates(stations_between)

	for station_coordinate in station_coordinates:
		ROUTE_NODES.append(station_coordinate)

	ROUTE_NODES.append(END_COORDINATES)

	min_travel_times = generate_min_travel_times(CURRENT_TIME, ROUTE_NODES, TRAVEL_MEANS)

	print(dp_reader(min_travel_times, ROUTE_NODES))

	# edges = generate_edges(nodes, TRAVEL_MEANS)
	return 



# Process directed graph to find the quickest route to destination
def process_graph(route_nodes):
	return




print(calculate_route([37.7798, -122.4039], [37.8616, -122.256523],[1,1,0,0,0,1]))
# print(calculate_route([37.880082, -122.274871], [37.879170, -122.269055],[1,1,0,0,0,1]))

# print(generate_nodes([37.7798, -122.403], [37.8716, -122.258423]))


