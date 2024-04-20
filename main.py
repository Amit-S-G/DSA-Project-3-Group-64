import sys
import osmnx as ox
from queue import PriorityQueue
from geopy.geocoders import Nominatim
from math import inf



'''







shortest_path = bfs_shortest_path(G, start_node, end_node)

if shortest_path is not None:
    # Calculate the length of the road between the two nodes
    road_length = sum(ox.distance.great_circle(G.nodes[shortest_path[i]]['y'], G.nodes[shortest_path[i]]['x'], G.nodes[shortest_path[i + 1]]['y'], G.nodes[shortest_path[i + 1]]['x']) for i in range(len(shortest_path) - 1))
    print("The length of the road between the two nodes is:", road_length)
else:
    print("No path found between the provided addresses.")

node_sizes = {start_node: 15, end_node: 15}
'''









city_bbox = 29.7241, 29.5801, -82.2558, -82.4289

# Initializing the walking network!
G = ox.graph_from_place("Gainesville, Florida", network_type="walk")
ox.convert.to_undirected(G)


def check_address(address, G):
    # Create an object from the Nominatim library that can convert addresses to lat and lng
    geoGuesser = Nominatim(user_agent="DSAGroup64")
    # Convert the passed in address to lat and lng
    location = geoGuesser.geocode(address)
    # If this was successful; that is, if the address is real and can be converted into coordinates
    if location:
        # Check to see that the coordinates are within the city's general bounding box.
        # This *might* change to be, like, France in general, because the bounding boxes for cities are tough to get down.
        if 29.7241 > location.latitude and location.latitude > 29.5801 and -82.2558 > location.longitude and location.longitude > -82.4289:
            # If the location is in bounds, find the node nearest it and return it
            node = ox.distance.nearest_nodes(G, location.longitude, location.latitude)
            return node
        else:
            # If the location is out of bounds, return nothing
            return None
    # If the conversion to coordinates did not work, return nothing
    else:
        return None


# Define Breadth-First Search function
def bfs_shortest_path(G, startNode_id, endNode_id):
    # Initialize a queue for BFS
    toVisit = []
    # Keep track of visited nodes
    visited = set()
    # Empty dict of nodes and their parents
    parents = {}
    toVisit.append(startNode_id)
    visited.add(startNode_id)

    # BFS algorithm
    while toVisit: # Continues loop until queue is empty
        # Let's get the current node's ID
        currNode = toVisit.pop(0)
        # If this is the node we want, break out of BFS
        if currNode == endNode_id:
            break
        # Else explore neighbors of the current node
        for neighbor in G.neighbors(currNode):
            # Checks if neighbor has not been visited
            if neighbor not in visited:
                # Grab the information about the edge between currNode and neighbors
                edge_data = G.get_edge_data(currNode, neighbor)
                single_edge_data = list(edge_data.values())[0]
                edge_id = single_edge_data['osmid']
                edge_length = single_edge_data['length']
                toVisit.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = (currNode, edge_id, edge_length)

    # If we did the traversal and never reached endNode, return None
    if currNode != endNode_id:
        return None
    # If we did find it
    else:
        total_length = 0
        # Iterate through the parents dict to retrace the path
        while (currNode != startNode_id):
            # Add the length of the edge used to reach currNode
            total_length += parents[currNode][2]
            currNode = parents[currNode][0]
        return total_length, parents










def a_star_search(startNode_id, endNode_id, G):
    # Create an empty dict of node scores
    node_scores = {}
    # Empty dict of nodes and their parents
    parents = {}
    for node_id in list(G.nodes()):
        # A* uses a "H"euristic cost (straight-line distance to goal), "G"iven cost (cost of path so far), and "F"inal cost
        # Every node will have an initial F, G, and H score of infinity, except the start node, for which they will be 0
        if node_id != startNode_id:
            # F, G, and H, IN THAT ORDER
            node_scores[node_id] = [inf, inf, inf]
        else:
            node_scores[node_id] = [0, 0, 0]
    # Create a PQ and Set for to_visit and Visited
    to_visit = PriorityQueue()
    visited = set()
    visited.add(startNode_id)
    # Put the starting node in there
    to_visit.put((node_scores[startNode_id][0], startNode_id))
    currNode = startNode_id
    while not to_visit.empty():
        currNode = to_visit.get()[1]
        if currNode == endNode_id:
            break
        for neighbor in G.neighbors(currNode):
            # Find each neighbor's straight line distance to the target
            node_scores[neighbor][2] = ox.distance.euclidean(G.nodes[neighbor]["y"], G.nodes[neighbor]["x"], G.nodes[endNode_id]["y"], G.nodes[endNode_id]["x"])
            # If the neighbor has not been visited
            if neighbor not in visited:
                # Iterate through every edge connecting currNode to neighbor
                # Get_edge_data returns a "dict mapping edge keys to attribute dicts for each edge" (from networkx doc)
                edge_data = G.get_edge_data(currNode, neighbor)
                # For edge in the dict of edges
                for edge in edge_data:
                    # Extract the length of the edge.
                    # Using list makes the dict convert into a list we can iterate without knowing the edge IDs
                    # Index [edge] finds the current dict we want, and then ['length'] gets this edge's length
                    edge_length = list(edge_data.values())[edge]['length']
                    if node_scores[currNode][1] + edge_length < node_scores[neighbor][1]:
                        node_scores[neighbor][1] = node_scores[currNode][1] + edge_length
                        # Does the same thing as getting the length above
                        edge_id = list(edge_data.values())[edge]['osmid']
                        parents[neighbor] = (currNode, edge_id)
                        node_scores[neighbor][0] = node_scores[neighbor][1] + node_scores[neighbor][2]
                        visited.add(neighbor)
                        to_visit.put((node_scores[neighbor][0], neighbor))


    # Now we've exited, meaning that currNode is now the endNode
    totalWeight = node_scores[currNode][1]
    return totalWeight, parents

'''
def uniform_cost_search(startNode_id, endNode_id, G):
    # Create an empty dict of node scores
    node_scores = {}
    # Empty dict of nodes and their parents
    parents = {}
    for node_id in list(G.nodes()):
        # Every node will have a running cost, as Uniform Cost Search will use that running cost to figure out where to go
        if node_id != startNode_id:
            # F, G, and H, IN THAT ORDER
            node_scores[node_id] = [inf, inf, inf]
        else:
            node_scores[node_id] = [0, 0, 0]
    # Create a PQ and Set for to_visit and Visited
    to_visit = PriorityQueue()
    visited = set()
    visited.add(startNode_id)
    # Put the starting node in there
    to_visit.put((node_scores[startNode_id][0], startNode_id))
    currNode = startNode_id
    while not to_visit.empty():
        currNode = to_visit.get()[1]
        if currNode == endNode_id:
            break
        for neighbor in G.neighbors(currNode):
            # If the neighbor has not been visited
            node_scores[neighbor][2] = ox.distance.euclidean(G.nodes[neighbor]["y"], G.nodes[neighbor]["x"], G.nodes[endNode_id]["y"], G.nodes[endNode_id]["x"])
            if neighbor not in visited:
                edge_data = G.get_edge_data(currNode, neighbor)
                for edge in edge_data:
                    # Extract the length of the edge
                    edge_length = list(edge_data.values())[0]['length']
                    if node_scores[currNode][1] + edge_length < node_scores[neighbor][1]:
                        node_scores[neighbor][1] = node_scores[currNode][1] + edge_length
                        edge_id = list(edge_data.values())[0]['osmid']
                        parents[neighbor] = (currNode, edge_id)
                        node_scores[neighbor][0] = node_scores[neighbor][1] + node_scores[neighbor][2]
                        visited.add(neighbor)
                        to_visit.put((node_scores[neighbor][0], neighbor))


    # Now we've exited, meaning that currNode is now the endNode
    totalWeight = node_scores[currNode][1]
    return totalWeight, parents
'''


def main():

    address = input("Enter an starting address: ")
    startNode = check_address(address, G)
    if startNode:
        print("Sounds good!")
    else:
        print("Sorry, that address either doesn't exist, or it isn't in Gainesville. Rerun!")
        sys.exit()

    address = input("Enter an destination address: ")
    endNode = check_address(address, G)
    if endNode:
        print("Sounds good!")
    else:
        print("Sorry, that address either doesn't exist, or it isn't in Gainesville. Rerun!")
        sys.exit()

    print(a_star_search(startNode, endNode, G)[0])

    # Create a node size dictionary
    node_sizes = {startNode: 15, endNode: 15}

    # Set size 0 for all other nodes
    for node in G.nodes():
        if node not in node_sizes:
            node_sizes[node] = 0

    print(bfs_shortest_path(G, startNode, endNode)[0])

    #fig, ax = ox.plot_graph(G, node_size=[node_sizes[node] for node in G.nodes()], show=False, save=True, filepath='street_map.png')


if __name__ == "__main__":
    main()
