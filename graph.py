from collections import defaultdict
from heapq import *
from bart_api import*
from google_maps_api import*
from uber_api import*
import time
import numpy


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

def generate_nodes(coords, transport_modes):
    current_time = time.time()
    nodes = []
    for i, n in enumerate(coords):
        nodes.append(Node(n[0], n[1], 0))
    return nodes

def first_bart_times(transport_modes, coords):
    start = Node(coords[0][0], coords[0][1], 0)
    fbart = Node(coords[1][0], coords[1][1], 0)
    times = []
    funcs = [
        walk_helper,
        bike_helper,
        car_helper,
        uber_helper,
        #lyft_helper,
        ]
    times = [f([start], [fbart]) for i, f in enumerate(funcs) if transport_modes[i] ]
    retval = set()
    for l in times:
        t = l[0]
        travel_times = get_bart_travel_time(t, get_nearest_station(start), get_nearest_station(fbart))
        for i in travel_times:
            retval.add(i[0])
    return list(travel_times)




            


    


def generate_edges(nodes, transport_modes):
    return None
def get_optimal_route(now, nodes, transport_modes):
    weights = generate_edge_weights(nodes, transport_modes)
    start = nodes[0]
    destination = nodes[-1]
    return dijkstra(start, destination, weights)

# This function returns the shortest path between start and end node.
# Arguments:
#   s, e: start and end location nodes
#   w: defaultdict representing weight of edges
# Return:
#   [type list[tuples (cost, n)]]
#   representing the time to get to the next node n
def dijkstra(s, e, w):
    fringe, visited, mins = [(0, s, ())], set(), {s: 0}
    while fringe:
        (cost, v, path) = heappop(fringe)
        if v not in visited:
            visited.add(v)
            path = (v, path)
            if v == e:
                return (cost, path)
            for c, nb in w.get(v, ()):
                if nb in visited: continue
                prev_low_cost = mins.get(nb, None)
                new_low_cost = cost + c
                if prev_low_cost is None or new_low_cost < prev_low_cost:
                    mins[nb] = new_low_cost
                    heappush(fringe, (new_low_cost, nb, path))
    return None

# This function generates the best weight for each edge given the available
# modes of transportation.
# Arguments:
#   nodes: list of nodes
#   transport_modes: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type defaultdict]
#   mapping node -> list of (cost, neighbor)

# def generate_edge_weights(nodes, transport_modes):
#     edges = []
#     for i, n in enumerate(nodes):
#         for j, n2 in enumerate(nodes[i:]):
#             w = calculate_best_weight(n, n2, transport_modes)
#             edges.append((n, n2, w))
#     g = defaultdict(list)
#     for l,r,c in edges:
#         g[l].append((c,r))
#     return g

def generate_edge_weights(nodes, transport_modes):
    edges = []

    
    car_template = car_template_helper(nodes)
    for i, n in enumerate(nodes):
        destinations = nodes[i:]
        origins = [n]*len(destinations)

        w = calculate_best_weight(origins, destinations, transport_modes)
        for j, n2 in enumerate(destinations):
            edges.append((n, n2, w[j]))
    
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))
    return g

def car_template_helper(nodes):
    wait_time_template = []
    for i, n in enumerate(nodes):
        wait_time_template.append((n, nodes[len(nodes)- 1]))
    return wait_time_template


#node class storing bart stations
#contains lat, lon values
#isBart boolean
#estimateArrival time adds tra
class Node:
    def __init__(self, lat, lon, bartTime):
        self.lat = lat
        self.lon = lon
        self.station = get_nearest_station(lat, lon)
        self.bartTime = bartTime #epoc
        self.traveled = [0, 0, 0, 0, 0, 0]
        self.transport_modes = [0, 0, 0, 0, 0, 0]



# This function returns the lowest weight between two nodes among the
# potential modes of transportation.
# Arguments:
#   origins, destinations: start and end location node arrays
#   tm: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type integer]
#   weight of edge in seconds

def calculate_best_weight(origins, destinations, tm):
    t = time.time()
    funcs = [
        walk_helper,
        bike_helper,
        car_helper,
        uber_helper,
        lyft_helper,
        bart_helper
    ]
    weights = []
    for i, f in enumerate(funcs):
        if tm[i]:
            if i == 3: #if uber, pass in weights to look at car travel times
                weights.append(f(origins, destinations, weights))
            else:
                weights.append(f(origins, destinations))
        else:
            weights.append(float('inf') * len(origins))

    # weights = \
    #     [(f(origins, destinations, t) if tm[i] else float('inf')) for i, f in enumerate(funcs)]
    weights = matrix(weights)

#POSSIBLE FORMAT BUG

    return weights.T


# def walk_helper(node1, node2, time):
#     n1 = (node1.lat, node1.lon)
#     n2 = (node2.lat, node2.lon)
#     print("walk_helper_result:{}".format(walk_travel_time(n1, n2)[1]))
#     return walk_travel_time(n1, n2)[1]


# def bike_helper(node1, node2, time):
#     n1 = (node1.lat, node1.lon)
#     n2 = (node2.lat, node2.lon)
#     print("bike_travel_result:{}".format(bike_travel_time(n1, n2)[1]))
#     return bike_travel_time(n1, n2)[1]



# def car_helper(node1, node2, time):
#     n1 = (node1.lat, node1.lon)
#     n2 = (node2.lat, node2.lon)
#     print("car_travel_result:{}".format(car_travel_time(n1, n2)[1]))
#     return car_travel_time(n1, n2)[1]


# def uber_helper(node1, node2, time):
#     return u_get_travel_time(node1.lat, node1.lon, node2.lat, node2.lon)[1]


# def lyft_helper(node1, node2, time):
#     return float("inf")

# def bart_helper(node1, node2, time): #time arrived at node1
#     n1 = get_nearest_station(node1.lat, node1.lon)
#     n2 = get_nearest_station(node2.lat, node2.lon)
#     if n1 == n2:
#         return 0
#     t = b_get_travel_time(time, n1[1], n2[1])
#     print(t)
#     return t[0]


#Each helper method takes in a list of corresponding origin and destination nodes
#Time is dummy for all helpers besides bart
def walk_helper(origins, destinations):
    o = []
    print(origins, destinations)
    for i in range(0, len(origins)):
        o.append((origins[i].lat, origins[i].lon))
    d = []
    for i in range(0, len(destinations)):
        d.append((destinations[i].lat, destinations[i].lon))
    #print("walk_helper_result:{}".format(walk_travel_time(n1, n2)[1]))
    retarr = time_to_seconds_batch(walk_travel_time(o, d))
    return retarr


def bike_helper(origins, destinations):
    o = []
    for i in range(0, len(origins)):
        o.append((origins[i].lat, origins[i].lon))
    d = []
    for i in range(0, len(destinations)):
        d.append((destinations[i].lat, destinations[i].lon))
    retarr = time_to_seconds_batch(bike_travel_time(o, d))
    return retarr


def car_helper(origins, destinations):
    o = []
    for i in range(0, len(origins)):
        o.append((origins[i].lat, origins[i].lon))
    d = []
    for i in range(0, len(destinations)):
        d.append((destinations[i].lat, destinations[i].lon))
    retarr = time_to_seconds_batch(car_travel_time(o, d))
    print("retarr", retarr)

    return retarr


#Uber travel time = car travel time + wait time
def uber_helper(origins, destinations, weights):

    #if no car time entry instantiated, write it 
    car_time = None
    if weights[2][0] == float('inf'):
        car_time = car_helper(origins, destinations, time)
    car_time = weights[2]
    print("car time", car_time)

    #calling uber API on first pair of origin-destination
    uber_travel_time = get_uber_travel_time(origins[0].lat, origins[1].lon, destinations[0].lat, destinations[1].lon)
    wait_time = uber_travel_time[1] - car_time[0]
    
    return [ct + wait_time for ct in car_time]


def lyft_helper(node1, node2):
    return float("inf")

#estimated time arrived at node1
def bart_helper(origins, destinations):


    n1 = get_nearest_station(node1.lat, node1.lon)
    n2 = get_nearest_station(node2.lat, node2.lon)
    if n1 == n2:
        return 0
    t = get_bart_travel_time(time, n1[1], n2[1])
    print("bart travel time", t)
    return t[0]

def time_to_seconds(time_str): # "x hours y mins" to seconds
    parse = time_str.split(' ')
    retval = 0

    if len(parse) == 4:
        retval += int(parse[0]) * 3600 + int(parse[2]) * 60
    elif len(parse) == 2:
        retval += int(parse[0]) * 60
    else:
        print("time_str: " + time_str + " not in x hours y mins format")
        
        return
    return retval

def time_to_seconds_batch(time_str_arr):
    retarr = []
    for t in time_str_arr:
        retarr.append(time_to_seconds(t))
    return retarr

    

    

if __name__ == "__main__":
    edges = [
        ("A", "B", 7),
        ("A", "D", 5),
        ("B", "C", 8),
        ("B", "D", 9),
        ("B", "E", 7),
        ("C", "E", 5),
        ("D", "E", 15),
        ("D", "F", 6),
        ("E", "F", 8),
        ("E", "G", 9),
        ("F", "G", 11)
    ]
    n1 = (37.8716, -122.272, 1)
    n2 = (37.7749, -122.4194, 1)
    n3 = (37.8512, -122.3131, 1)
    n4 = (37.8012, -122.3010, 1)
    nodes = [n1, n2, n3, n4]
    origins = [n1, n2]
    destinations= [n3, n4]
    transport_modes = [1, 1, 1, 1, 1, 1]
    test = first_bart_times(transport_modes, nodes)
    print("=== Graph Generation Test ===")
    print(test)

    # print("=== Dijkstra Test ===")
    # edge_weights = generate_edge_weights(nodes, transport_modes)
    # print(edge_weights)
    # print("A -> E:")
    # print(dijkstra("A", "E", edge_weights))
    # print("F -> G:")
    # print(dijkstra("F", "G", edge_weights))

    # print("=== Optimal Route Test ===")
    # now = time.time()
    # print(calculate_best_weight(origins, destinations, transport_modes))
    # #edges = generate_edge_weights(nodes, transport_modes)
    #print(edges
    #print get_optimal_route(now, nodes, transport_modes)


