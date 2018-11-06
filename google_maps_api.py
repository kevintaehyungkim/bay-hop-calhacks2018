import json
import urllib
import googlemaps
from datetime import datetime
from configparser import SafeConfigParser

config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

GOOGLE_MAPS_API_KEY = config_parser.get('GoogleMapsAPI', 'key')

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


def parseEpoch(text):
		parts = text.split(' ')
		time = 0
		if len(parts) == 4:
			time += int(parts[0]) * 60 * 60
			time += int(parts[2]) * 60
		elif len(parts) == 2:
			time += int(parts[0]) * 60
		else:
			raise Exception('text parsing failed')
		return time


# Travel time from origins to destinations via car
# origins/destinations are arrays of tuples of latitude/longitude pairs
def car_travel_time(origins, destinations):

	origins_str = ""
	destinations_str = ""
	car_travel_time_arr = []

	for origin in origins:
		origins_str += str(origin[0]) + "," + str(origin[1]) + "|"

	for destination in destinations:
		destinations_str += "" + str(destination[0]) + "," + str(destination[1]) + "|"

	origins_str = origins_str[:-1]
	destinations_str = destinations_str[:-1]

	query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origins_str + "&destinations=" + destinations_str + "&departure_time=now" + "&mode=driving&key=" + GOOGLE_MAPS_API_KEY

	data = json.loads(urllib.request.urlopen(query).read().decode("utf-8"))["rows"]

	for d in data:
		# print(d)
		if "duration_in_traffic" in d["elements"][0].keys():
			regular_time = parseEpoch(d["elements"][0]["duration"]["text"])
			traffic_time = parseEpoch(d["elements"][0]["duration_in_traffic"]["text"])
			car_travel_time_arr.append(regular_time+traffic_time)
		else:
			car_travel_time_arr.append(parseEpoch(d["elements"][0]["duration"]["text"]))

	return car_travel_time_arr


# Travel time from origins to destinations via biking
# origins/destinations are arrays of tuples of latitude/longitude pairs
def bike_travel_time(origins, destinations):
	origins_str = ""
	destinations_str = ""
	bike_travel_time_arr = []

	for origin in origins:
		origins_str += "" + str(origin[0]) + "," + str(origin[1]) + "|"

	for destination in destinations:
		destinations_str += "" + str(destination[0]) + "," + str(destination[1]) + "|"

	origins_str = origins_str[:-1]
	destinations_str = destinations_str[:-1]

	query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origins_str + "&destinations=" + destinations_str + "&mode=bicycling&key=" + GOOGLE_MAPS_API_KEY

	data = json.loads(urllib.request.urlopen(query).read().decode("utf-8"))["rows"]

	for d in data:
		bike_travel_time_arr.append(parseEpoch(d["elements"][0]["duration"]["text"]))

	return bike_travel_time_arr


# Travel time from origins to destinations via walking
# origins/destinations are arrays of tuples of latitude/longitude pairs
def walk_travel_time(origins, destinations):
	origins_str = ""
	destinations_str = ""
	walk_travel_time_arr = []

	for origin in origins:
		origins_str += "" + str(origin[0]) + "," + str(origin[1]) + "|"

	for destination in destinations:
		destinations_str += "" + str(destination[0]) + "," + str(destination[1]) + "|"

	origins_str = origins_str[:-1]
	destinations_str = destinations_str[:-1]

	query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origins_str + "&destinations=" + destinations_str + "&mode=walking&key=" + GOOGLE_MAPS_API_KEY

	data = json.loads(urllib.request.urlopen(query).read().decode("utf-8"))["rows"]

	for d in data:
		walk_travel_time_arr.append(parseEpoch(d["elements"][0]["duration"]["text"]))

	return walk_travel_time_arr

def geocode(address):
	addressparts = address.split(' ')
	address_str = ''
	for part in addressparts:
		address_str += part + '+'
	address_str = address_str[:-1]
	query = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address_str + "&key=" + GOOGLE_MAPS_API_KEY

	data = json.loads(urllib.request.urlopen(query).read().decode("utf-8"))["results"][0]['geometry']['location']
	return (data['lat'], data['lng'])


# print(walk_travel_time([[37.8716, -122.258423],[37.8716, -122.258423]], [[37.7798, -122.4039],[37.7798, -122.4039]]))
print(car_travel_time([[37.8616, -122.256523]], [[37.7798, -122.4039]]))
# geocode('Berkeley, CA')
# print(car_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))
# print(bike_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))


# import simplejson, urllib
# orig_coord = 37.8716, -122.258423
# dest_coord = 37.7798, -122.4039
# url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
# result= simplejson.load(urllib.urlopen(url))
# driving_time = result['rows'][0]['elements'][0]['duration']['value']

# print(driving_time)





