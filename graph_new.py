#new graph.py

#wrapper function to generate graph
#Arguments:
#   coords: list of coordinates of start, all barts inbetween, and end, arr of tuples
#   transport_modes is boolean array length 6 to indicate accepted modes
#   [walk, bike, car uber, lyft, bart]
#Return:
#   generated graph

class Node:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.station = get_nearest_station(lat, lon)
        self.bartTime = 0 #epoch
        self.traveled = [0, 0, 0, 0, 0, 0]
        self.transport_modes = [0, 0, 0, 0, 0, 0]

def generate_graph(coords, transport_modes):

    #generate nodes with all bartTimes set to 0
    nodes = generate_nodes(coords, transport_modes)

    #generate edges
    return

#Generate nodes with lat and lon
#No bart time yet, fill in later
def generate_nodes(coords, transport_modes):
    current_time = time.time()
    nodes = []
    for i, n in enumerate(coords):
        nodes.append(Node(n[0], n[1]))
    return nodes

def set_bart_time():
    return None

def first_bart_time(coords, transport_modes):
    