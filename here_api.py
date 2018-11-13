import json
import grequests


def get_distance(coords):
	print(coords)
	origin_str = str(coords[0][0]) + ',' + str(coords[0][1])
	destination_str = str(coords[1][0]) + ',' + str(coords[1][1])
	query = "https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0=" + origin_str + "&waypoint1=" + destination_str + "&mode=fastest%3Bcar%3Btraffic%3Aenabled&app_id=devportal-demo-20180625&app_code=9v2BkviRwi9Ot26kp2IysQ&departure=now"
	print(query)
	responses = [grequests.get(u) for u in [query]]

	distance = 0

	for r in grequests.map(responses):
		# print(r.json()["response"]["route"][0]["summary"]["distance"])
		distance = float(r.json()["response"]["route"][0]["summary"]["distance"])

	distance_km = float(str(distance/1000.0).split('.')[0] + '.' + str(distance/1000.0).split('.')[1][:2])
	distance_mi = float(str(distance/1609.34).split('.')[0] + '.' + str(distance/1609.34).split('.')[1][:2])

	distance_result = [distance_km, distance_mi]

	return distance_result

# print(get_distance([[37.7798, -122.4039], [37.8719, -122.2585]]))
