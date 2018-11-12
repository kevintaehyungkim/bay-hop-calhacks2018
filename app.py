from flask import Flask, flash, redirect, url_for, request, render_template, json, session, abort
import routing
import time
import google_maps_api

from routing import *


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/route', methods=['POST'])
def route():
	if request.method == 'POST':
		form = request.form
		start = form['start']
		dest = form['destination']
		geocode_start_dest = google_maps_api.geocode([start, dest])
		geocode_start = geocode_start_dest[0]
		geocode_dest = geocode_start_dest[1]

		results = {'start': start, 'end': dest, 'startLat': geocode_start[0], 'startLng': geocode_start[1], 'endLat': geocode_dest[0], 'endLng': geocode_dest[1]}
		route_info = generate_graph([results['startLat'],results['startLng']], [results['endLat'],results['endLng']], [0,0,0,0,1])

		# [[0, 59], [['S', 'Powell St.', 'W'], ['Powell St.', '12th St. Oakland City Center', 'B'], ['12th St. Oakland City Center', 'Downtown Berkeley', 'B'], ['Downtown Berkeley', 'E', 'W']]]


		
		route_nodes = route_info[1]
		route_nodes[0][0] = form['start']
		route_nodes[len(route_nodes)-1][1] = form['destination']

		return render_template('results.html', results=results, route_info=route_info)
	else:
		return redirect(url_for('home'))


if __name__ == '__main__':
   app.run()


