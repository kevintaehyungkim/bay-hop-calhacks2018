import json
import time
import urllib.request
import grequests
import multiprocessing as mp
from math import sin, cos, sqrt, atan2, radians, inf
from configparser import SafeConfigParser
from time import strftime

config_parser = SafeConfigParser()
config_parser.read('station_info.cfg')


RADIUS_EARTH = 6378.137
BART_STATIONS = grequests.map([grequests.get("http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y")])[0].json()["root"]["stations"]["station"]

LINES = []
k=time.time()
line_urls = ["http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=1&key=MW9S-E7SL-26DU-VV8V&json=y",
				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=3&key=MW9S-E7SL-26DU-VV8V&json=y",
				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=5&key=MW9S-E7SL-26DU-VV8V&json=y",
				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=7&key=MW9S-E7SL-26DU-VV8V&json=y",
				"http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=11&key=MW9S-E7SL-26DU-VV8V&json=y"]
responses = [grequests.get(u) for u in line_urls]
for r in grequests.map(responses):
	LINES.append(list(r.json()["root"]["routes"]["route"]["config"]["station"]))
q = time.time()
print(q-k)


# pool = mp.Pool(len(modes))
# 	travel_data = list(pool.map(send_request,urls))

# 	pool.close()
# 	pool.join()

# for i in range(len(travel_data)):
# 	# print(data)
# 	travel_time_arr = []
# 	data = travel_data[i]["rows"]


# Returns the nearest BART Station given a latitude and longitude
def get_nearest_station(coord_pair_arr):
	nearest_stations = []
	global BART_STATIONS
	for i in range(0,len(coord_pair_arr)):
		nearest_station = ""
		station_abbreviation = ""
		lat = coord_pair_arr[i][0]
		lon = coord_pair_arr[i][1]
		current_shortest_distance = float('inf')

		for station in BART_STATIONS: 
			lat1 = radians(lat)
			lon1 = radians(lon)
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

		nearest_stations.append([nearest_station, station_abbreviation])

	return nearest_stations

# Inputs: current epoch time, starting station abbreviation, end station abbreviation
# Returns: An array of index-2 arrays containing start and end epoch time of journey (up to next 2 departures)
def get_bart_travel_time(current_date_time, current_epoch_time, start_station_abbrs, end_station_abbrs):
	total = {}
	urls = []

	current_time_str = strftime("%I:%M %p", current_date_time)

	for i in range(0,len(start_station_abbrs)):
		start_station_abbr = start_station_abbrs[i]
		end_station_abbr = end_station_abbrs[i]

		urls.append("http://api.bart.gov/api/sched.aspx?cmd=depart&orig={0}&dest={1}&time={2}&date=now&key=MW9S-E7SL-26DU-VV8V&b=0&a=4&l=0&json=y".format(start_station_abbr, end_station_abbr, current_time_str))

	responses = [grequests.get(u) for u in urls]

	for r in grequests.map(responses):
		travel_times_arr = []
		upcoming_bart_rides = r.json()["root"]["schedule"]["request"]["trip"]
		travel_times_arr.append(upcoming_bart_rides[0]["@origin"] + ' ' + upcoming_bart_rides[0]["@destination"])

		for bart_ride in upcoming_bart_rides:
			bart_ride_time = bart_ride["@origTimeMin"]
			bart_ride_date = bart_ride["@origTimeDate"]
			print(bart_ride["@destTimeMin"])
			print(bart_ride["@destTimeDate"])

			pattern = '%m/%d/%Y %I:%M %p'
			bart_epoch = int(time.mktime(time.strptime(bart_ride_date + ' ' + bart_ride_time, pattern)))

			if bart_epoch > current_epoch_time:
				travel_times_arr.append([int(time.mktime(time.strptime(bart_ride_date + ' ' + bart_ride_time, pattern))), 
					int(time.mktime(time.strptime(bart_ride["@destTimeDate"] + ' ' + bart_ride["@destTimeMin"], pattern)))])

		total[travel_times_arr[0]] = travel_times_arr[1:]

	return total


# Returns a list of BART stations in between the start and end station
def get_stations_between(start_station, dest_station):

	global LINES

	all_routes = []
	exchange_stations = {"MCAR", "BAYF", "WOAK"}

	# Check all lines if if both stations in one single line
	for line in LINES: 
		if start_station in line and dest_station in line:
			start_station_index = line.index(start_station)
			dest_station_index = line.index(dest_station)
			if start_station_index < dest_station_index:
				return line[start_station_index:dest_station_index+1]
			else:
				return list(reversed(line[dest_station_index:start_station_index+1]))

	# Find stations between the route of two stations that need to exchange lines
	for current_line in LINES: 
		if start_station in current_line:
			start_station_index = current_line.index(start_station)
			for i in range(0,len(current_line)):
				station = current_line[i]
				if station in exchange_stations:
					for next_line in LINES: 
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
# def get_arrival_times(current_time, stations):
# 	arrival_times = [[], []]
# 	length = len(stations)
# 	if length == 0:
# 		return arrival_times

# 	travel_times = get_bart_travel_time(current_time, stations[0], stations[1])

# 	arrival_times[0].append(travel_times[0][0])
# 	arrival_times[1].append(travel_times[1][0])

# 	time1 = travel_times[0][1]
# 	time2 = travel_times[1][1]
# 	for i in range(1, length-1):
# 		travel_times1 = get_bart_travel_time(time1, stations[i], stations[i+1])
# 		travel_times2 = get_bart_travel_time(time2, stations[i], stations[i+1])

# 		arrival_times[0].append(travel_times1[0][0])
# 		arrival_times[1].append(travel_times2[0][0])

# 		time1 = travel_times1[0][1]
# 		time2 = travel_times2[0][1]

# 	return arrival_times

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



# line_urls = ["http://api.bart.gov/api/stn.aspx?cmd=stns&key=MW9S-E7SL-26DU-VV8V&json=y"]
# responses = [grequests.get(u) for u in line_urls]
# for r in grequests.map(responses):
# 	for station in (list(r.json()["root"]["stations"]["station"])):
# 		print("[" + station["abbr"] + "]")
# 		print("name: " + station["name"])
# 		print("\n")







