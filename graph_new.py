#new graph.py

#wrapper function to generate graph
#Arguments:
#   coords: list of coordinates of start, all barts inbetween, and end, arr of tuples
#   transport_modes is boolean array length 6 to indicate accepted modes
#   [walk, bike, car uber, lyft, bart]
#Return:
#   generated graph

def generate_graph(coords, transport_modes):

    #generate nodes
    nodes = generate_nodes(coords, transport_modes)

    #generate edges
    return