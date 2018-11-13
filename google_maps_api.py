import json
import googlemaps
import grequests
import time
import multiprocessing as mp
from datetime import datetime
from configparser import SafeConfigParser


config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

GOOGLE_MAPS_API_KEY = config_parser.get('GoogleMapsAPI', 'key')

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


# def travel_distance(coords):
# 	distance = 0
# 	query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origins_str + "&destinations=" + destinations_str + "&mode=" + travel_mode + "&departure_time=now" + "&key=" + GOOGLE_MAPS_API_KEY
# 	responses = [grequests.get(u) for u in urls]

# 	for r in grequests.map(responses):
# 		upcoming_bart_rides = r.json()["rows"]["elements"]["distance"]
# 		travel_times_arr.append(upcoming_bart_rides[0]["@origin"] + ' ' + upcoming_bart_rides[0]["@destination"])

def travel_time(modes, coords):

	print(coords)

	urls = []
	transportation_modes = ['walking', 'bicycling', 'driving']
	total = {}

	origins_str = ""
	destinations_str = ""
	travel_time_arr = []
	batch_size = 10
	num_batches = 0

	for mode in modes:
		origins_str = ""
		destinations_str = ""
		for i in range(0,len(coords)-1,batch_size):
			origins_str = ""
			origins_batch = coords[i:i+batch_size]

			for j in range(i+1,len(coords),batch_size):
				destinations_str = ""
				dest_batch = coords[j:j+batch_size]
				num_batches += 1

				for origin in origins_batch:
					origins_str += "" + str(origin[0]) + "," + str(origin[1]) + "|"

				for dest in dest_batch:
					destinations_str += "" + str(dest[0]) + "," + str(dest[1]) + "|"

				origins_str = origins_str[:-1]
				destinations_str = destinations_str[:-1]

				travel_mode = transportation_modes[mode]
				query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origins_str + "&destinations=" + destinations_str + "&mode=" + travel_mode + "&departure_time=now" + "&key=" + GOOGLE_MAPS_API_KEY
				urls.append(query)

	pool = mp.Pool(len(modes))
	travel_data = list(pool.map(send_request,urls))

	pool.close()
	pool.join()

	# TODO: handle batch 
	print(num_batches)

	for i in range(len(travel_data)):
		# print(data)
		travel_time_arr = []
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
		total[transportation_modes[modes[i]]] = travel_time_arr

	return total


def send_request(url):
	try:
		return grequests.map([grequests.get(url)])[0].json()
	except e as Exception:
		print (e)

def geocode(addresses):
	urls = []
	total = []

	for address in addresses:
		addressparts = address.split(' ')
		address_str = ''
		for part in addressparts:
			address_str += part + '+'
		address_str = address_str[:-1]
		urls.append("https://maps.googleapis.com/maps/api/geocode/json?address=" + address_str + "&key=" + GOOGLE_MAPS_API_KEY)

	pool = mp.Pool(len(addresses))
	geocode_data = pool.map(send_request,urls)

	pool.close()
	pool.join()

	for data in geocode_data:
		d = data["results"][0]['geometry']['location']
		total.append((d['lat'], d['lng']))

	return total


# print(walk_travel_time([[37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.7798, -122.4039], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.784471, -122.407974], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.789405, -122.401066], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.792874, -122.39702], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.804872, -122.29514], [37.803768, -122.27145], [37.803768, -122.27145], [37.803768, -122.27145], [37.803768, -122.27145], [37.803768, -122.27145], [37.80835, -122.268602], [37.80835, -122.268602], [37.80835, -122.268602], [37.80835, -122.268602], [37.829065, -122.26704], [37.829065, -122.26704], [37.829065, -122.26704], [37.852803, -122.270062], [37.852803, -122.270062], [37.870104, -122.268133]], [[37.784471, -122.407974], [37.789405, -122.401066], [37.792874, -122.39702], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.789405, -122.401066], [37.792874, -122.39702], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.792874, -122.39702], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.804872, -122.29514], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.803768, -122.27145], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.80835, -122.268602], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.829065, -122.26704], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.852803, -122.270062], [37.870104, -122.268133], [37.8616, -122.256523], [37.870104, -122.268133], [37.8616, -122.256523], [37.8616, -122.256523]]))

# embarcadero to 923 folsom walk
# print(travel_time([0], [[37.7929, -122.3971]]))

# geocode('Berkeley, CA')
# print(car_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))
# print(bike_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))




