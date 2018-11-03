from flask import Flask, flash, redirect, url_for, request, render_template, json, session, abort
import routing
import google_maps_api
app = Flask(__name__)

# @app.route('/')
# def hello_world():
#    return "Hello World"

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/route', methods=['POST'])
def route():
	if request.method == 'POST':
		form = request.form
		start = form['start']
		dest = form['destination']
		geocodeStart = google_maps_api.geocode(start)
		geocodeDest = google_maps_api.geocode(dest)
		print(start)
		print(dest)
		print(geocodeStart)
		print(geocodeDest)
		# routing.py calls

		results = {'start': start, 'end': dest, 'startLat': geocodeStart[0], 'startLng': geocodeStart[1], 'endLat': geocodeDest[0], 'endLng': geocodeDest[1]}
		return render_template('results.html', results=results)
	else:
		return redirect(url_for('home'))


if __name__ == '__main__':
   app.run()




# TAKE OUT BUS, NODE COMPLEXITY
# CALL API every time for each node, a lot of computing power

# MULTIPLE NODES FOR EACH BART STATION BASED ON TIME, ex. can't make bart in 3 minutes because 5 min walk, but taking bart ultimately faster than uber across bridge
# LIMIT 3 next bart rides
# EACH NODE HAS A CATEGORY(TYPE) - identifier to plan directed edges from this node to the next during generation

# https://www.gps-coordinates.net/
# https://www.gps-coordinates.net/api

# CAR -> BART -> CAR X
# BIKE -> CAR/UBER X
