import json
import urllib
import googlemaps
import multiprocessing as mp
from datetime import datetime
from configparser import SafeConfigParser

import grequests
import time

config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

GOOGLE_MAPS_API_KEY = config_parser.get('GoogleMapsAPI', 'key')

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


def travel_time(modes, origins, destinations):

	urls = []
	transportation_modes = ['walking', 'bicycling', 'driving']
	total = {}

	origins_str = ""
	destinations_str = ""
	travel_time_arr = []

	for origin in origins:
		origins_str += "" + str(origin[0]) + "," + str(origin[1]) + "|"

	for destination in destinations:
		destinations_str += "" + str(destination[0]) + "," + str(destination[1]) + "|"

	origins_str = origins_str[:-1]
	destinations_str = destinations_str[:-1]

	for mode in modes:
		travel_mode = transportation_modes[mode]
		query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origins_str + "&destinations=" + destinations_str + "&mode=" + travel_mode + "&departure_time=now" + "&key=" + GOOGLE_MAPS_API_KEY
		urls.append(query)

	travel_data = []
	pool = mp.Pool(len(modes))
	travel_data = pool.map(send_request,urls)

	pool.close()
	pool.join()

	for i in range(len(travel_data)):
		data = travel_data[i]["rows"]
		if modes[i] == 2:
			for row in data:
				distances = row["elements"]
				for d in distances:
					travel_time_arr.append(d["duration_in_traffic"]["value"])
		else:
			for row in data:
				distances = row["elements"]
				for d in distances:
					travel_time_arr.append(d["duration"]["value"])
		total[transportation_modes[i]] = travel_time_arr

	return total


def send_request(url):
	return grequests.map([grequests.get(url)])[0].json()

def geocode(address):
	addressparts = address.split(' ')
	address_str = ''
	for part in addressparts:
		address_str += part + '+'
	address_str = address_str[:-1]
	query = "https://maps.googleapis.com/maps/api/geocode/json?address=" + address_str + "&key=" + GOOGLE_MAPS_API_KEY

	data = json.loads(urllib.request.urlopen(query).read().decode("utf-8"))["results"][0]['geometry']['location']
	return (data['lat'], data['lng'])


# print(walk_travel_time([[37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.803768, -122.27145], [37.803768, -122.27145], [37.803768, -122.27145], [37.803768, -122.27145], [37.803768, -122.27145], [37.80835, -122.268602], [37.80835, -122.268602], [37.80835, -122.268602], [37.80835, -122.268602], [37.829065, -122.26704], [37.829065, -122.26704], [37.829065, -122.26704], [37.852803, -122.270062], [37.852803, -122.270062], [37.870104, -122.268133]], [[37.784471, -122.407974], [37.789405, -122.401066], [37.792874, -122.39702], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.789405, -122.401066], [37.792874, -122.39702], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.792874, -122.39702], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.870104, -122.268133], [37.8616, -122.256523], [37.8616, -122.256523]]))

# embarcadero to 923 folsom walk
# print(walk_travel_time([[37.7929, -122.3971]],[[37.7798, -122.4039]]))

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








