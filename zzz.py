from multiprocessing import Process
from multiprocessing import Pool
import multiprocessing as mp



import json
import datetime
import time
import urllib.request
from math import sin, cos, sqrt, atan2, radians, inf
from configparser import SafeConfigParser

# def f(name):
#     print 'hello', name

# if __name__ == '__main__':
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()

# def get_bart_travel_time(a):

# 	start_station_abbr = 'DBRK'
# 	end_station_abbr = 'POWL'

# 	travel_times_arr = []
# 	# try:
# 	upcoming_bart_rides = json.loads(urllib.request.urlopen("http://api.bart.gov/api/sched.aspx?cmd=depart&orig={0}&dest={1}&date=now&key=MW9S-E7SL-26DU-VV8V&b=0&a=4&l=1&json=y".format(start_station_abbr, end_station_abbr)).read().decode("utf-8"))["root"]["schedule"]["request"]["trip"]
# 	for bart_ride in upcoming_bart_rides:
# 		bart_ride_time = bart_ride["@origTimeMin"]
# 		bart_ride_time_split = bart_ride_time.split()
# 		bart_ride_date = bart_ride["@origTimeDate"]

# 		if bart_ride_time_split[1] == 'PM':
# 			bart_ride_time_split = bart_ride_time_split[0].split(':')
# 			bart_ride_time_split[0] = str(int(bart_ride_time_split[0]) + 12)
# 		else:
# 			bart_ride_time_split = bart_ride_time_split[0].split(':')

# 		bart_date = bart_ride_date + str(bart_ride_time_split[0]) + ':' + str(bart_ride_time_split[1]) + ":" + "00"
# 		pattern = '%m/%d/%Y %H:%M:%S'
# 		bart_epoch = int(time.mktime(time.strptime(bart_date, pattern)))
# 		current_time = time.time()
# 		if bart_epoch > current_time:
# 			travel_times_arr.append([bart_ride["@origTimeMin"], bart_ride["@destTimeMin"], ])
# 	# except:
# 	# 	print("BART API Request Error")
# 	# print(travel_times_arr)
# 	return travel_times_arr

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

def get_lyft_pickup_time(z):

	start_latitude, start_longitude, ride_type = z

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
	else:
		print(response.status_code)
		print(response.json.get('error'))
		print(response.json.get('error_description'))




# a = time.time()
# print(get_bart_travel_time(time.time(), 'DBRK', 'POWL'))
# b = time.time()
# print(b-a)


# a = time.time()

# zzzz = [time.time()]
# zzzzz = ['DBRK']
# zzzzzz = ['POWL']

# num_workers = mp.cpu_count()  

# pool = mp.Pool(num_workers)
# for task in tasks:
#     pool.apply_async(target = func, args = (task,))
# print(mp.cpu_count())
# pool = Pool(processes=180)  

arrayz = []
for i in [4,8,12,16,20,40,80]:
	print(i)
	a = time.time()
	pool = Pool(processes=i)  
	bbb = [[37.880082, -122.274871, None]]*20
	pool.map(get_lyft_pickup_time, bbb)
	b = time.time()
	arrayz.append(b-a)

print(arrayz)




# b = time.time()
# print(b-a)



# a = time.time()
# get_bart_travel_time('POWL')
# b = time.time()
# print(b-a)


# a = time.time()
# get_lyft_pickup_time([37.880082, -122.274871, None])
# b = time.time()
# print(b-a)




# print(datetime.datetime.now())
#  from multiprocessing import Pool
# >>> p = Pool(5)
# >>> def f(x):
# ...     return x*x
# ...
# >>> p.map(f, [1,2,3])













