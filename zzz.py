from multiprocessing import Process
from multiprocessing import Pool



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

def get_bart_travel_time(a):

	start_station_abbr = 'DBRK'
	end_station_abbr = 'POWL'

	travel_times_arr = []
	# try:
	upcoming_bart_rides = json.loads(urllib.request.urlopen("http://api.bart.gov/api/sched.aspx?cmd=depart&orig={0}&dest={1}&date=now&key=MW9S-E7SL-26DU-VV8V&b=0&a=4&l=1&json=y".format(start_station_abbr, end_station_abbr)).read().decode("utf-8"))["root"]["schedule"]["request"]["trip"]
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
		current_time = time.time()
		if bart_epoch > current_time:
			travel_times_arr.append([bart_ride["@origTimeMin"], bart_ride["@destTimeMin"], ])
	# except:
	# 	print("BART API Request Error")
	# print(travel_times_arr)
	return travel_times_arr




# a = time.time()
# print(get_bart_travel_time(time.time(), 'DBRK', 'POWL'))
# b = time.time()
# print(b-a)


a = time.time()

zzzz = [time.time()]
zzzzz = ['DBRK']
zzzzzz = ['POWL']

pool = Pool(processes=50)  
bbb = [1,2]*500
pool.map(get_bart_travel_time, bbb)



b = time.time()
print(b-a)


# a = time.time()
# print(get_bart_travel_time('POWL'))
# b = time.time()
# print(b-a)




# print(datetime.datetime.now())
#  from multiprocessing import Pool
# >>> p = Pool(5)
# >>> def f(x):
# ...     return x*x
# ...
# >>> p.map(f, [1,2,3])













