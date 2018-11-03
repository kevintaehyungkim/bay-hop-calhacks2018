from collections import defaultdict
from heapq import *
import time

#from uber_api import get_travel_time
#from bart_api import get_nearest_station, get_destination_station, get_travel_time

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
def generate_edge_weights(nodes, transport_modes):
    edges = []
    for i, n in enumerate(nodes):
        for j, n2 in enumerate(nodes[i:]):
            w = calculate_best_weight(n, n2, transport_modes)
            edges.append((n, n2, w))
    print edges
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))
    return g

# This function returns the lowest weight between two nodes among the
# potential modes of transportation.
# Arguments:
#   s, e: start and end location nodes
#   tm: transport modes as a bit array
#   [WALK, BIKE, CAR, UBER, LYFT, BART]
# Return:
#   [type integer]
#   weight of edge in seconds
def calculate_best_weight(s, e, tm):
    funcs = [
        walk_helper,
        bike_helper,
        car_helper,
        uber_helper,
        lyft_helper,
        bart_helper
    ]
    weights = \
        [(f(s, e) if tm[i] else float('inf')) for i, f in enumerate(funcs)]
    return min(weights)

def walk_helper(node1, node2):
    return 1

def bike_helper(node1, node2):
    return 2

def car_helper(node1, node2):
    return 3

def uber_helper(node1, node2):
    return 4

def lyft_helper(node1, node2):
    return 5

def bart_helper(node1, node2):
    return 6

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
    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    transport_modes = [1, 1, 1, 1, 1, 1]

    print "=== Dijkstra Test ==="
    edge_weights = generate_edge_weights(nodes, transport_modes)
    print edge_weights
    print "A -> E:"
    print dijkstra("A", "E", edge_weights)
    print "F -> G:"
    print dijkstra("F", "G", edge_weights)

    print "=== Optimal Route Test ==="
    now = time.time()
    print calculate_best_weight(nodes[0], nodes[1], transport_modes)
    #edges = generate_edge_weights(nodes, transport_modes)
    #print edges
    #print get_optimal_route(now, nodes, transport_modes)
