from configparser import SafeConfigParser

from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session
from lyft_rides.client import LyftRidesClient

config_parser = SafeConfigParser()
config_parser.read('api_keys.cfg')

LYFT_CLIENT_ID = config_parser.get('LyftAPI', 'id')
LYFT_CLIENT_SECRET = config_parser.get('LyftAPI', 'secret')
LYFT_PERMISSION_SCOPES = config_parser.get('LyftAPI', 'scopes')

auth_flow = ClientCredentialGrant(
    LYFT_CLIENT_ID,
    LYFT_CLIENT_SECRET,
    LYFT_PERMISSION_SCOPES
    )
session = auth_flow.get_session()

# Returns the fastest travel means offered by Uber and its duration in seconds
def get_lyft_pickup_time(start_latitude, start_longitude, ride_type=None):
	client = LyftRidesClient(session)

	response = client.get_pickup_time_estimates( 
	    start_latitude,
	    start_longitude,
	    ride_type
	)

	if response.status_code == 200:
		eta_estimates = response.json.get('eta_estimates')

		etas = {}

		for eta in eta_estimates:
			ride_type = eta['display_name']
			eta_seconds = eta['eta_seconds']
			valid_estimate = eta['is_valid_estimate']
			if valid_estimate and eta_seconds is not None:
				etas[ride_type] = eta_seconds

		if 'Lyft' in etas.keys():
			return ['Lyft', etas['Lyft']]
		elif len(etas.keys()) > 0:
			fastest_ride_option = min(etas, key=etas.get)
			return [fastest_ride_option, etas[fastest_ride_option]]
		else:
			return ['No rides available', float('inf')]

print(get_lyft_pickup_time(37.7798, -122.403))





