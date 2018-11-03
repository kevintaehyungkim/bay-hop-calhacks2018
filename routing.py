# Base-URL: http://localhost:5000/

from flask import Flask
from flask import Markup
from flask import Flask, flash, redirect, url_for, request, render_template, json, session, abort

from uber_api import get_uber_travel_time
from bart_api import get_nearest_station, get_bart_travel_time, get_stations_between, get_station_coordinates

import time

# START_COORDINATES = [37.8716, -122.258423]
# END_COORDINATES = [37.7798, -122.4039]

CURRENT_TIME = 0
START_COORDINATES = []
END_COORDINATES = []

# INDEX: WALK, BIKE, CAR, UBER, LYFT, BART
MEANS_OF_TRANSPORATION = []

ROUTE_NODES = []

# Provides the quickest routes from current location to destination using provided travel means
def calculate_route(current, destination, travel_means):
	# convert to coordinates: maybe add method in google maps api to generate coordinates from an address
	# Inputs -
	# current: current address
	# destination: destination address
	# travel_means: array of travel methods selected by the user
	CURRENT_TIME = time.time()
	TRAVEL_MEANS = travel_means
	# START_COORDINATES = #
	# END_COORDINATES = #
	generate_nodes(current, destination)
	#process_nodes
	return 

# Generates nodes based on start and end coordinates provided
def generate_nodes(START_COORDINATES, END_COORDINATES): 
	# starting location (first node)
	ROUTE_NODES.append(START_COORDINATES)
	# if no need to take bart, add that in later 
	start_station = get_nearest_station(START_COORDINATES[0], START_COORDINATES[1])
	end_station = get_nearest_station(END_COORDINATES[0], END_COORDINATES[1])
	stations_between = get_stations_between(start_station[1], end_station[1])
	station_coordinates = get_station_coordinates(stations_between)

	for station_coordinate in station_coordinates:
		ROUTE_NODES.append(station_coordinate)

	ROUTE_NODES. append(END_COORDINATES)

	generate_graph(ROUTE_NODES)


# Generates directed graph based on input nodes
def generate_graph(route_nodes):


	return 

# Process directed graph to find the quickest route to destination
def process_graph(route_nodes):
	return



############################################################
###################### HELPER METHODS ######################
############################################################

# Returns the total travel time (wait time + travel time) from starting 
# location to destination via uber
# def uber_travel_time(start, destination):
# 	print (start)
# 	print(destination)
# 	return get_travel_time(start[0], start[1], destination[0], destination[1])

# # Returns travel time to reach the destination via walking
# def walk_travel_time(start, destination):
# 	return

# # Returns travel time to reach the destination via bike 
# def bike_travel_time(start, destination):
# 	return

# # Returns a nested array containing departure and arrival times of the
# # next three bart rides from starting station to the destination station
# # Input: Strings of the abbreviations for starting station and end station
# def bart_travel_time(station_start, station_end):
# 	return get_travel_times(station_start, station_end)


# uber wait duration
# fix bug not as many options depending on location
# uber_wait_duration = get_wait_duration(START_COORDINATES[0], START_COORDINATES[1], END_COORDINATES[0], END_COORDINATES[1])
# print(uber_wait_duration)

# nearest_station = get_nearest_station(START_COORDINATES[0], START_COORDINATES[1])
# print (nearest_station)

# destination_station = get_destination_station(END_COORDINATES[0], END_COORDINATES[1])
# print(destination_station)
# #nearest bart station

# zzz = get_travel_time(nearest_station[1], destination_station[1])
# print (zzz)

print(generate_nodes([37.7798, -122.403], [37.8716, -122.258423]))


