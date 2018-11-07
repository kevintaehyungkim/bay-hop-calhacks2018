import json
import datetime
import time
import urllib.request
from math import sin, cos, sqrt, atan2, radians, inf
from configparser import SafeConfigParser

config_parser = SafeConfigParser()
config_parser.read('station_info.cfg')

# BART_API_KEY = config_parser.get('BartAPI', 'key')
RADIUS_EARTH = 6378.137

# Returns the nearest BART Station given a latitude and longitude
def get_nearest_station(latitude, longitude):
	nearest_station = ""
	station_abbreviation = ""
	current_shortest_distance = float('inf')

	try:
		BART_STATIONS = json.loads(urllib.request.urlopen("http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y").read().decode("utf-8"))["root"]["stations"]["station"]

		for station in BART_STATIONS: 
			lat1 = radians(latitude)
			lon1 = radians(longitude)

			# print(lat1)

			lat2 = radians(float(station["gtfs_latitude"]))
			lon2 = radians(float(station["gtfs_longitude"]))

			dlon = lon2 - lon1
			dlat = lat2 - lat1

			a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
			c = 2 * atan2(sqrt(a), sqrt(1 - a))

			distance = RADIUS_EARTH * c

			if distance < current_shortest_distance:
				nearest_station = station["name"]
				station_abbreviation = station["abbr"]
				current_shortest_distance = distance
	except Exception as e:
		print("BART API Request Error")
		print(e)


	return [nearest_station, station_abbreviation]

# Inputs: current epoch time, starting station abbreviation, end station abbreviation
# Returns: An array of index-2 arrays containing start and end epoch time of journey (up to next 2 departures)
def get_bart_travel_time(current_date_time, current_epoch_time, start_station_abbr, end_station_abbr):
	travel_times_arr = []
	# current_date_time = time.localtime(current_epoch_time)

	if current_date_time.tm_hour == 12:
		if current_date_time.tm_min < 10:
			current_time_str = "" + str(current_date_time.tm_hour - 12) + ":" + "0" + str(current_date_time.tm_min) + "pm"
		else:
			current_time_str = "" + str(current_date_time.tm_hour - 12) + ":" + str(current_date_time.tm_min) + "pm"
	elif current_date_time.tm_hour >= 12:
		if current_date_time.tm_min < 10:
			current_time_str = "" + str(current_date_time.tm_hour - 12) + ":" + "0" + str(current_date_time.tm_min) + "pm"
		else:
			current_time_str = "" + str(current_date_time.tm_hour - 12) + ":" + str(current_date_time.tm_min) + "pm"
	else:
		if current_date_time.tm_min < 10:
			current_time_str = "" + str(current_date_time.tm_hour) + ":" + "0" + str(current_date_time.tm_min) + "am"
		else:
			current_time_str = "" + str(current_date_time.tm_hour) + ":" + str(current_date_time.tm_min) + "am"


	try:
		upcoming_bart_rides = json.loads(urllib.request.urlopen("http://api.bart.gov/api/sched.aspx?cmd=depart&orig={0}&dest={1}&time={2}&date=now&key=MW9S-E7SL-26DU-VV8V&b=0&a=4&l=0&json=y".format(start_station_abbr, end_station_abbr, current_time_str)).read().decode("utf-8"))["root"]["schedule"]["request"]["trip"]
		
		for bart_ride in upcoming_bart_rides:
			bart_ride_time = bart_ride["@origTimeMin"]
			bart_ride_time_split = bart_ride_time.split()
			bart_ride_date = bart_ride["@origTimeDate"]

			if bart_ride_time_split[1] == 'PM':
				bart_ride_time_split = bart_ride_time_split[0].split(':')
				bart_ride_time_split[0] = str(int(bart_ride_time_split[0]) + 12)
			else:
				bart_ride_time_split = bart_ride_time_split[0].split(':')

			bart_date = bart_ride_date + str(bart_ride_time_split[0]) + ':' + str(bart_ride_time_split[1]) + ":" + "00"
			pattern = '%m/%d/%Y %H:%M:%S'
			bart_epoch = int(time.mktime(time.strptime(bart_date, pattern)))

			if bart_epoch >= current_epoch_time:
				travel_times_arr.append([bart_ride["@origTimeMin"], bart_ride["@destTimeMin"]])

		# TODO: PM TO AM TIME DIFF
		for i in range(len(travel_times_arr)):
			for j in range(len(travel_times_arr[i])):
				bart_ride_time_split = travel_times_arr[i][j].split()
				# print(bart_ride_time_split)
				if bart_ride_time_split[1] == 'PM':
					bart_ride_time_split = bart_ride_time_split[0].split(':')
					bart_ride_time_split[0] = str(int(bart_ride_time_split[0]) + 12)
				else:
					bart_ride_time_split = bart_ride_time_split[0].split(':')

				# print(bart_ride_time_split)

				bart_date = bart_ride_date + str(bart_ride_time_split[0]) + ':' + str(bart_ride_time_split[1]) + ":" + "00"
				pattern = '%m/%d/%Y %H:%M:%S'
				bart_epoch = int(time.mktime(time.strptime(bart_date, pattern)))

				travel_times_arr[i][j] = bart_epoch
	except Exception as e:
		print("BART API Request Error")
		print(e)

	return travel_times_arr


# Returns a list of BART stations in between the start and end station
def get_stations_between(start_station, dest_station):
	all_routes = []
	exchange_stations = {"MCAR", "BAYF", "WOAK"}
	try:
		line_1 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key=MW9S-E7SL-26DU-VV8V&json=y".format("1")).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_2 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key=MW9S-E7SL-26DU-VV8V&json=y".format("3")).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_3 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key=MW9S-E7SL-26DU-VV8V&json=y".format("5")).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_4 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key=MW9S-E7SL-26DU-VV8V&json=y".format("7")).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_5 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key=MW9S-E7SL-26DU-VV8V&json=y".format("11")).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]

		lines  = [list(line_1), list(line_2), list(line_3), list(line_4), list(line_5)]

		# Check all lines if if both stations in one single line
		for line in lines: 
			if start_station in line and dest_station in line:
				start_station_index = line.index(start_station)
				dest_station_index = line.index(dest_station)
				if start_station_index < dest_station_index:
					return line[start_station_index:dest_station_index+1]
				else:
					return list(reversed(line[dest_station_index:start_station_index+1]))

		# Find stations between the route of two stations that need to exchange lines
		for current_line in lines: 
			if start_station in current_line:
				start_station_index = current_line.index(start_station)
				for i in range(0,len(current_line)):
					station = current_line[i]
					if station in exchange_stations:
						for next_line in lines: 
							if next_line != current_line and station in next_line and dest_station in next_line:
								exchange_station_index = next_line.index(station)
								dest_station_index = next_line.index(dest_station)
								if start_station_index < i:
									route = current_line[start_station_index:i]
									if exchange_station_index < dest_station_index:
										route += next_line[exchange_station_index:dest_station_index+1]
									else:
										route += list(reversed(next_line[dest_station_index:exchange_station_index+1]))
									all_routes.append(route)
								else:
									route = list(reversed(current_line[i+1:start_station_index+1]))
									if exchange_station_index < dest_station_index:
										route += next_line[exchange_station_index:dest_station_index+1]
									else:
										route += list(reversed(next_line[dest_station_index:exchange_station_index+1]))
									all_routes.append(route)
							else:
								continue
					else:
						continue
			else:
				continue

		return min(all_routes)

	except Exception as e:
		print("BART API Request Error")
		print(e)

	return all_routes


# Helper method to return BART stations in between the start and end station
def get_stations_between_helper(current_route, routes, exchange_stations, dest_station, prev_route):  
	if not current_route:
		return 
	elif dest_station in current_route:
		dest_station_index = current_route.index(dest_station)
		return route[0:dest_station_index]
	else:
		for i in range(0,len(current_route)):
			station = current_route[i]
			if station in exchange_stations:
				for next_route in routes:
					if station in next_route and next_route != prev_route and dest_station in next_route:
						station_index = next_route.index(station)
						dest_station_index = next_route.index(dest_station)
						if station_index < dest_station_index:
							return current_route[0:i+1] + next_route[station_index:dest_station_index+1]
						else: 
							return current_route[0:i+1] + list(reversed(next_route[station_index:dest_station_index+1]))
					else:
						continue
			else:
				continues
	return 

# Given an array of station abbreviations, return the latitude and longitude for each station in order
def get_station_coordinates(stations):
	if not stations:
		return []

	station_coordinate_arr = []

	for station in stations:
		station_lat = config_parser.get(station, 'latitude')
		station_long = config_parser.get(station, 'longitude')
		station_coordinate_arr.append([station_lat, station_long])
	
	return station_coordinate_arr

# return two lists of arrival times
def get_arrival_times(current_time, stations):
	arrival_times = [[], []]
	length = len(stations)
	if length == 0:
		return arrival_times

	travel_times = get_bart_travel_time(current_time, stations[0], stations[1])

	arrival_times[0].append(travel_times[0][0])
	arrival_times[1].append(travel_times[1][0])

	time1 = travel_times[0][1]
	time2 = travel_times[1][1]
	for i in range(1, length-1):
		travel_times1 = get_bart_travel_time(time1, stations[i], stations[i+1])
		travel_times2 = get_bart_travel_time(time2, stations[i], stations[i+1])

		arrival_times[0].append(travel_times1[0][0])
		arrival_times[1].append(travel_times2[0][0])

		time1 = travel_times1[0][1]
		time2 = travel_times2[0][1]

	return arrival_times

#################
##### TESTS #####
#################

# GET_STATIONS_BETWEEN
# print(get_stations_between("DBRK", "POWL"))
# print(get_stations_between("DBRK", "ANTC"))
# print(get_stations_between("WARM", "ANTC"))
# print(get_stations_between("WARM", "DUBL"))
# print(get_stations_between("MLBR", "ANTC"))

# GET_TRAVEL_TIME
# print (time.time())
# print(get_bart_travel_time(1541305980, 'POWL', 'MCAR'))
# print(get_bart_travel_time(1541305980, 'POWL', 'DBRK'))
# print(get_bart_travel_time(1541305980, 'POWL', 'WOAK'))

# print(time.time())

# GET_NEAREST_STATION
# print(get_nearest_station(37.8716, -122.258423)) 
# print(get_nearest_station(37.7798, -122.4039)) 

# BART_STATIONS = json.loads(urllib.request.urlopen("http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y").read().decode("utf-8"))["root"]["stations"]["station"]
# print(BART_STATIONS)

# print (get_station_coordinates(['POWL', 'MONT', 'EMBR', 'WOAK', '12TH', '19TH', 'MCAR', 'ASHB', 'DBRK']))

# get_arrival_times(time.time(), ['POWL', 'MONT', 'EMBR', 'WOAK', '12TH', '19TH', 'MCAR', 'ASHB', 'DBRK'])

