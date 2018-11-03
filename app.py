from flask import Flask, flash, redirect, url_for, request, render_template, json, session, abort
import routing
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
		cLoc = form['currentLocation']
		dest = form['destination']
		print(cLoc)
		print(dest)
		# routing.py calls
		results = {'start': cLoc, 'end': dest}
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
