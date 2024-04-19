import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import networkx as nx
from geopy.geocoders import Nominatim
from collections import deque

# Define Breadth-First Search function
def bfs_shortest_path(graph, start, end):
    # Initialize a queue for BFS
    queue = deque([(start, [start])]) # tuple containing start node and a list containing start node
    visited = set()  # Keep track of visited nodes

    # BFS algorithm
    while queue: # continues loop until queue is empty
        node, path = queue.popleft() # dequeues the first element (node, path) from the queue
        visited.add(node) # adds current node to the set of visited nodes

        # If the current node is the destination, return the path
        if node == end: # checks if current node is the destination node
            return path # returns path if it is

        # Explore neighbors of the current node
        for neighbor in graph[node]: # iterates over each neighboring node
            if neighbor not in visited: # checks if neighbor has not been visited
                queue.append((neighbor, path + [neighbor])) # added to queue along with the path taken to reach it

    # If no path is found, return None
    return None

def check_address(G, address, geolocator):
    location = geolocator.geocode(address)
    nearest_node = ox.distance.nearest_nodes(G, location.longitude, location.latitude)
    return nearest_node

# Prompt user for start and end addresses
start_address = input("Enter the start address: ")
end_address = input("Enter the end address: ")

# Get the graph for the specified location
G = ox.graph_from_place("Gainesville, Florida", network_type="walk")

# Convert the graph to undirected
G = ox.convert.to_undirected(G)

# Initialize geocoder
geolocator = Nominatim(user_agent="DSAGroup69")

# Find the nearest node to the start address
start_node = check_address(G, start_address, geolocator)
print("Nearest node to the start address:", start_node)

# Find the nearest node to the end address
end_node = check_address(G, end_address, geolocator)
print("Nearest node to the end address:", end_node)

# Find the shortest path between the start and end nodes using BFS
shortest_path = bfs_shortest_path(G, start_node, end_node)

if shortest_path is not None:
    # Calculate the length of the road between the two nodes
    road_length = sum(ox.distance.great_circle(G.nodes[shortest_path[i]]['y'], G.nodes[shortest_path[i]]['x'], G.nodes[shortest_path[i + 1]]['y'], G.nodes[shortest_path[i + 1]]['x']) for i in range(len(shortest_path) - 1))
    print("The length of the road between the two nodes is:", road_length)
else:
    print("No path found between the provided addresses.")

node_sizes = {start_node: 15, end_node: 15}

for node in G.nodes():
    if node not in node_sizes:
        node_sizes[node] = 0

ox.plot.plot_graph_route(G, node_size=[node_sizes[node] for node in G.nodes()], route=shortest_path, show=False, save=True, filepath='street_map.png')
