from configparser import SafeConfigParser

from uber_rides.session import Session
from uber_rides.client import UberRidesClient

config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

UBER_API_KEY = config_parser.get('UberAPI', 'key')

# Returns the fastest travel means offered by Uber and its duration in seconds
def get_uber_travel_time(start_latitude, start_longitude, end_latitude, end_longitude):
	session = Session(server_token=UBER_API_KEY)
	client = UberRidesClient(session)

	response = client.get_price_estimates( 
	    start_latitude,
	    start_longitude,
	    end_latitude,
	    end_longitude,
	    seat_count=1
	)

	ride_estimates = response.json.get('prices')

	trip_durations = {}

	for ride_estimate in ride_estimates:
		display_name = ride_estimate['display_name']
		travel_duration = ride_estimate['duration']
		trip_durations[display_name] = travel_duration

	if 'UberX' in trip_durations.keys():
		return ['UberX', trip_durations['UberX']]

	fastest_ride_option = min(trip_durations, key=trip_durations.get)
	return [fastest_ride_option, trip_durations[fastest_ride_option]]


# print(get_uber_travel_time(37.7798, -122.403, 37.8716, -122.258423))


# https://developer.lyft.com/v1/reference#availability-driver-eta
# https://pypi.org/project/lyft_rides/


# curl -H 'Authorization: Token oYNTpD7SO55UT-ynUYkFnDlA_OgKWRU7cM03BdRZ' \
#      -H 'Accept-Language: en_US' \
#      -H 'Content-Type: application/json' \
#      'https://api.uber.com/v1.2/estimates/time?start_latitude=37.7752315&start_longitude=-122.418075'