import googlemaps
from datetime import datetime
from configparser import SafeConfigParser

config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

GOOGLE_MAPS_API_KEY = config_parser.get('GoogleMapsAPI', 'key')

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Travel time from start to destination via car
def car_travel_time(start, destination):
	origin_coord = str(start[0]) + ',' + str(start[1])
	dest_coord = str(destination[0]) + ',' +str(destination[1])

	now = datetime.now()
	directions_result = gmaps.directions(str(origin_coord),
	                                     str(dest_coord),
	                                     mode="driving",
	                                     avoid="ferries",
	                                     traffic_model= 'pessimistic',
	                                     departure_time=now
	                                    )

	distance = directions_result[0]['legs'][0]['distance']['text']
	travel_time = directions_result[0]['legs'][0]['duration']['text']

	return distance, travel_time


# Travel time from start to destination via biking
def bike_travel_time(start,destination):
	origin_coord = str(start[0]) + ',' + str(start[1])
	dest_coord = str(destination[0]) + ',' +str(destination[1])

	now = datetime.now()
	directions_result = gmaps.directions(str(origin_coord),
	                                     str(dest_coord),
	                                     mode="bicycling",
	                                     traffic_model= 'pessimistic',
	                                     departure_time=now
	                                    )

	distance = directions_result[0]['legs'][0]['distance']['text']
	travel_time = directions_result[0]['legs'][0]['duration']['text']

	return distance, travel_time


# Travel time from start to destination via walking
def walk_travel_time(start, destination):
	origin_coord = str(start[0]) + ',' + str(start[1])
	dest_coord = str(destination[0]) + ',' +str(destination[1])

	now = datetime.now()
	directions_result = gmaps.directions(str(origin_coord),
	                                     str(dest_coord),
	                                     mode="walking",
	                                     avoid="ferries",
	                                     traffic_model= 'pessimistic',
	                                     departure_time=now
	                                    )

	distance = directions_result[0]['legs'][0]['distance']['text']
	travel_time = directions_result[0]['legs'][0]['duration']['text']

	return distance, travel_time


print(car_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))
print(bike_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))
print(walk_travel_time([37.8716, -122.258423], [37.7798, -122.4039]))


# import simplejson, urllib
# orig_coord = 37.8716, -122.258423
# dest_coord = 37.7798, -122.4039
# url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str(orig_coord),str(dest_coord))
# result= simplejson.load(urllib.urlopen(url))
# driving_time = result['rows'][0]['elements'][0]['duration']['value']

# print(driving_time)



