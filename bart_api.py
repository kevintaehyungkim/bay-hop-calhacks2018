import json
import datetime
import time
import urllib.request
from math import sin, cos, sqrt, atan2, radians, inf
from configparser import SafeConfigParser

config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

BART_API_KEY = config_parser.get('BartAPI', 'key')
RADIUS_EARTH = 6378.137


def get_nearest_station(latitude, longitude):
	nearest_station = ""
	station_abbreviation = ""
	current_shortest_distance = float('inf')

	try:
		BART_STATIONS = json.loads(urllib.request.urlopen("http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y").read().decode("utf-8"))["root"]["stations"]["station"]

		for station in BART_STATIONS: 
			lat1 = radians(latitude)
			lon1 = radians(longitude)
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
	except:
		print("BART API Request Error")

	return [nearest_station, station_abbreviation, current_shortest_distance]


def get_bart_travel_time(current_time, start_station_abbr, end_station_abbr):
	travel_times_arr = []
	try:
		upcoming_bart_rides = json.loads(urllib.request.urlopen("http://api.bart.gov/api/sched.aspx?cmd=arrive&orig={0}&dest={1}&date=now&key=MW9S-E7SL-26DU-VV8V&b=0&a=4&l=1&json=y".format(start_station_abbr, end_station_abbr)).read().decode("utf-8"))["root"]["schedule"]["request"]["trip"]
		
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

			if bart_epoch > current_time:
				travel_times_arr.append([bart_ride["@origTimeMin"], bart_ride["@destTimeMin"], ])
	except:
		print("BART API Request Error")

	return travel_times_arr


# Returns a list of BART stations in between the start and end station
def get_stations_between(start_station, dest_station):
	all_routes = []
	exchange_stations = {"MCAR", "BAYF", "WOAK"}
	try:
		line_1 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key={1}&json=y".format("1", BART_API_KEY)).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_2 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key={1}&json=y".format("3", BART_API_KEY)).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_3 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key={1}&json=y".format("5", BART_API_KEY)).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_4 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key={1}&json=y".format("7", BART_API_KEY)).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]
		line_5 = json.loads(urllib.request.urlopen("http://api.bart.gov/api/route.aspx?cmd=routeinfo&route={0}&key={1}&json=y".format("11", BART_API_KEY)).read().decode("utf-8"))["root"]["routes"]["route"]["config"]["station"]

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

	except:
		print("BART API Request Error")

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


#################
##### TESTS #####
#################

# GET_STATIONS_BETWEEN
print(get_stations_between("DBRK", "POWL"))
# print(get_stations_between("DBRK", "ANTC"))
# print(get_stations_between("WARM", "ANTC"))
# print(get_stations_between("WARM", "DUBL"))
# print(get_stations_between("MLBR", "ANTC"))

# GET_TRAVEL_TIME
print(get_travel_time(time.time(), 'DBRK', 'POWL'))

# GET_NEAREST_STATION
print(get_nearest_station(37.8716, -122.258423)) 
# print(get_nearest_station(37.7798, -122.4039)) 

