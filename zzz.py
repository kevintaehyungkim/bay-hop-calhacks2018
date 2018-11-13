# from multiprocessing import Process
# from multiprocessing import Pool
# import multiprocessing as mp
# import queue


# import json
# import datetime
# import time
# import urllib.request
# from math import sin, cos, sqrt, atan2, radians, inf
# from configparser import SafeConfigParser

# qqq = queue.Queue(maxsize=0)

# # def f(name):
# #     print 'hello', name

# # if __name__ == '__main__':
# #     p = Process(target=f, args=('bob',))
# #     p.start()
# #     p.join()

# # def get_bart_travel_time(a):

# # 	start_station_abbr = 'DBRK'
# # 	end_station_abbr = 'POWL'

# # 	travel_times_arr = []
# # 	# try:
# # 	upcoming_bart_rides = json.loads(urllib.request.urlopen("http://api.bart.gov/api/sched.aspx?cmd=depart&orig={0}&dest={1}&date=now&key=MW9S-E7SL-26DU-VV8V&b=0&a=4&l=1&json=y".format(start_station_abbr, end_station_abbr)).read().decode("utf-8"))["root"]["schedule"]["request"]["trip"]
# # 	for bart_ride in upcoming_bart_rides:
# # 		bart_ride_time = bart_ride["@origTimeMin"]
# # 		bart_ride_time_split = bart_ride_time.split()
# # 		bart_ride_date = bart_ride["@origTimeDate"]

# # 		if bart_ride_time_split[1] == 'PM':
# # 			bart_ride_time_split = bart_ride_time_split[0].split(':')
# # 			bart_ride_time_split[0] = str(int(bart_ride_time_split[0]) + 12)
# # 		else:
# # 			bart_ride_time_split = bart_ride_time_split[0].split(':')

# # 		bart_date = bart_ride_date + str(bart_ride_time_split[0]) + ':' + str(bart_ride_time_split[1]) + ":" + "00"
# # 		pattern = '%m/%d/%Y %H:%M:%S'
# # 		bart_epoch = int(time.mktime(time.strptime(bart_date, pattern)))
# # 		current_time = time.time()
# # 		if bart_epoch > current_time:
# # 			travel_times_arr.append([bart_ride["@origTimeMin"], bart_ride["@destTimeMin"], ])
# # 	# except:
# # 	# 	print("BART API Request Error")
# # 	# print(travel_times_arr)
# # 	return travel_times_arr

# from configparser import SafeConfigParser

# from lyft_rides.auth import ClientCredentialGrant
# from lyft_rides.session import Session
# from lyft_rides.client import LyftRidesClient

# config_parser = SafeConfigParser()
# config_parser.read('api_keys.cfg')

# LYFT_CLIENT_ID = config_parser.get('LyftAPI', 'id')
# LYFT_CLIENT_SECRET = config_parser.get('LyftAPI', 'secret')
# LYFT_PERMISSION_SCOPES = config_parser.get('LyftAPI', 'scopes')

# auth_flow = ClientCredentialGrant(
#     LYFT_CLIENT_ID,
#     LYFT_CLIENT_SECRET,
#     LYFT_PERMISSION_SCOPES
#     )
# session = auth_flow.get_session()

# def get_lyft_pickup_time(z):

# 	start_latitude, start_longitude, ride_type = z

# 	client = LyftRidesClient(session)

# 	response = client.get_pickup_time_estimates( 
# 	    start_latitude,
# 	    start_longitude,
# 	    ride_type
# 	)

# 	if response.status_code == 200:
# 		eta_estimates = response.json.get('eta_estimates')

# 		etas = {}

# 		for eta in eta_estimates:
# 			ride_type = eta['display_name']
# 			eta_seconds = eta['eta_seconds']
# 			valid_estimate = eta['is_valid_estimate']
# 			if valid_estimate and eta_seconds is not None:
# 				etas[ride_type] = eta_seconds

# 		if 'Lyft' in etas.keys():
# 			return ['Lyft', etas['Lyft']]
# 		elif len(etas.keys()) > 0:
# 			fastest_ride_option = min(etas, key=etas.get)
# 			return [fastest_ride_option, etas[fastest_ride_option]]
# 		else:
# 			return ['No rides available', float('inf')]
# 	else:
# 		print(response.status_code)
# 		print(response.json.get('error'))
# 		print(response.json.get('error_description'))




# def zzz(z):

# 	start_latitude = z[0]
# 	start_longitude = z[1]
# 	d = z[2]
# 	ride_type = None

# 	client = LyftRidesClient(session)

# 	response = client.get_pickup_time_estimates( 
# 	    start_latitude,
# 	    start_longitude,
# 	    ride_type
# 	)

# 	if response.status_code == 200:
# 		eta_estimates = response.json.get('eta_estimates')

# 		etas = {}

# 		for eta in eta_estimates:
# 			ride_type = eta['display_name']
# 			eta_seconds = eta['eta_seconds']
# 			valid_estimate = eta['is_valid_estimate']
# 			if valid_estimate and eta_seconds is not None:
# 				etas[ride_type] = eta_seconds

# 		if 'Lyft' in etas.keys():
# 			d[start_latitude] = etas['Lyft']
# 			return ['Lyft', etas['Lyft']]
# 		elif len(etas.keys()) > 0:
# 			fastest_ride_option = min(etas, key=etas.get)
# 			return [fastest_ride_option, etas[fastest_ride_option]]
# 		else:
# 			return ['No rides available', float('inf')]
# 	else:
# 		print(response.status_code)
# 		print(response.json.get('error'))
# 		print(response.json.get('error_description'))




# # a = time.time()
# # print(get_bart_travel_time(time.time(), 'DBRK', 'POWL'))
# # b = time.time()
# # print(b-a)


# # a = time.time()

# # num_workers = mp.cpu_count()  

# # pool = mp.Pool(num_workers)
# # for task in tasks:
# #     pool.apply_async(target = func, args = (task,))
# # print(mp.cpu_count())
# # pool = Pool(processes=180)  

# # arrayz = []
# # for i in [64]:
# # 	a = time.time()
# # 	pool = Pool(processes=i)  
# # 	bbb = [[37.880082, -122.274871, None]]*48


# # 	with mp.Pool(24) as pool:
# # 		result_list = pool.map(get_lyft_pickup_time, bbb)
# # 		# print(result_list)


# # 	# pool.map(get_lyft_pickup_time, bbb)
# # 	b = time.time()
# # 	arrayz.append(b-a)

# # print(arrayz)



# # import threading
# # from threading import Thread
# # from multiprocessing.pool import ThreadPool
# # from multiprocessing import Process, Manager

# # def zzzz():

# # 	a = time.time()
# # 	for i in range(30):
# # 		Thread(target = zzz, args=[[QQ, 37.880082, -122.274871, None]]).start()
# # 		# pool = ThreadPool(processes=1)
# # 		# async_result = pool.apply_async(zzz, [[37.880082, -122.274871, None]])
# # 	b = time.time()
# # 	print(b-a)

# # zzzz()

# # def holyfk():

# # 	# global qqq
# # 	a = time.time()

# # 	# threads = [None] * 30
# # 	# results = [None] * 30

# # 	# for i in range(30):
# # 	#     threads[i] = Thread(target = zzz, args=[[37.880082, -122.274871, None]])
# # 	#     threads[i].start()
# # 	#     print(qqq.qsize())

# # 	manager = Manager()
# # 	d = manager.dict()

# # 	for i in range(4):
# # 		pro1 = mp.Process(target=zzz, args=[[37.880082, -122.274871, d]])
# # 		pro2 = mp.Process(target=zzz, args=[[37.880082, -122.274871, d]])
# # 		pro3 = mp.Process(target=zzz, args=[[37.880082, -122.274871, d]])
# # 		pro4 = mp.Process(target=zzz, args=[[37.880082, -122.274871, d]])
# # 		pro5 = mp.Process(target=zzz, args=[[37.880082, -122.274871, d]])
# # 		pro6 = mp.Process(target=zzz, args=[[37.880082, -122.274871, d]])

# # 		pro1.start()
# # 		pro2.start()
# # 		pro3.start()
# # 		pro4.start()
# # 		pro5.start()
# # 		pro6.start()

# # 		pro1.join()
# # 		pro2.join()
# # 		pro3.join()
# # 		pro4.join()
# # 		pro5.join()
# # 		pro6.join()

# # 	print(d)	

# # 	b = time.time()
# # 	print(b-a)

# # holyfk()











# # print(datetime.datetime.now())
# #  from multiprocessing import Pool
# # >>> p = Pool(5)
# # >>> def f(x):
# # ...     return x*x
# # ...
# # >>> p.map(f, [1,2,3])





# # fooResult = Queue.Queue()

# # def foo(num):
# # 	result = 0

# # 	if num>10:
# # 	result = 1
# # 	elif num>50:
# # 	result = 2

# # 	fooResult.put(result)

# # 	t = thread.start_new_thread(foo,(12,))

# # 	# do other stuff, foo is running in background

# # 	r = fooResult.get() # guaranteed to block until result is available
# # 	print r







# # https://stackoverflow.com/questions/2632520/what-is-the-fastest-way-to-send-100-000-http-requests-in-python







# import json
# import urllib
# import googlemaps
# from datetime import datetime
# from configparser import SafeConfigParser

# import grequests
# import requests
# import urllib3
# import time

# from requests_futures.sessions import FuturesSession


# # query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=37.7929,-122.3971&destinations=37.7798,-122.4039&mode=walking&key=AIzaSyAGPqfNcowbyMyUwhF9YNxL2qU4GdnpVwg"
# query = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=37.8694,-122.2719|37.870104,-122.268133|37.852803,-122.270062|37.829065,-122.26704|37.80835,-122.268602|37.803768,-122.27145|37.804872,-122.29514|37.792874,-122.39702|37.789405,-122.401066|37.784471,-122.407974&destinations=37.870104,-122.268133|37.852803,-122.270062|37.829065,-122.26704|37.80835,-122.268602|37.803768,-122.27145|37.804872,-122.29514|37.792874,-122.39702|37.789405,-122.401066|37.784471,-122.407974|37.7798,-122.4039&departure_time=now&mode=driving&key=AIzaSyAGPqfNcowbyMyUwhF9YNxL2qU4GdnpVwg"

# a = time.time()
# # data = urllib.request.urlopen(query)
# # for i in range(0,1):
# data = json.loads(urllib.request.urlopen(query).read().decode("utf-8"))
# b = time.time()

# print(b-a)





# # a=time.time()
# # urls = [query]*1
# # results = map(urllib.request.urlopen, urls)
# # # for r in results:
# # json.loads(list(results)[0].read().decode("utf-8"))
# # b = time.time()
# # print(b-a)



# import grequests



# urls = [query]*1
# a=time.time()

# rs = [grequests.get(u) for u in urls]
# grequests.map(rs)

# # rs = (grequests.get(u) for u in urls)
# # requests = grequests.imap(rs)
# # arr = []
# # for response in requests:
# # 	arr.append(response.data)
	
# b = time.time()
# print(b-a)

# # import httplib2


# # a=time.time()
# # # resp, content = httplib2.Http().request(query)
# # b = time.time()
# # print(b-a)


# # def ggg (url):
# # 	return urllib.request.urlopen(query).read().decode("utf-8")


# # arrayz = []

# # a = time.time()

# # bbb = [query]*3

# # with mp.Pool(24) as pool:
# # 	result_list = pool.map(ggg, bbb)
# # 	print("1")


# # # pool.map(get_lyft_pickup_time, bbb)
# # b = time.time()
# # arrayz.append(b-a)

# # print(arrayz)






# # # CURRENT_DATE_TIME = time.localtime(current_epoch_time)
# # # 	CURRENT_EPOCH_TIME = current_epoch_time











# # # import argparse
# # # import sys
# # # import time

# # # from multiprocessing.pool import Pool, ThreadPool

# # # def task(arg):
# # # 	for i in range(3):
# # # 		print("Working on", arg, "with i =", i)
# # # 		time.sleep(1)

# # # def main():
# # # 	parser = argparse.ArgumentParser()
# # # 	parser.add_argument('--delay', default=1, type=float)
# # # 	args = parser.parse_args()

# # # 	thread_pool = ThreadPool(processes=1)

# # # 	thread_pool.apply_async(task, (0,))
# # # 	thread_pool.apply_async(task, (1,))
# # # 	time.sleep(args.delay)

# # # 	print("Terminating")
# # # 	thread_pool.terminate()
# # # 	print("Termination: Initiated")
# # # 	thread_pool.join() # Does not return.
# # # 	print("Termination: Done")


# # # try:
# # # 	sys.exit(main())
# # # except KeyboardInterrupt:
# # # 	sys.exit('\nInterrupted')

















import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyC5_ShaibPjbrctDcI8vXgDUtI3ua-E814')

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall, Parramatta, NSW, Sydney Town Hall, ",
                                     "Parramatta, NSW Sydney Town Hall",
                                     mode="transit",
                                     departure_time=now)

print(directions_result)




