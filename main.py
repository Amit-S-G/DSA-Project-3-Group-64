import sys
import osmnx as ox
from queue import PriorityQueue
from geopy.geocoders import Nominatim
from math import inf


# Initializing the walking network!
G = ox.graph_from_place("Paris, France", network_type="walk")
ox.convert.to_undirected(G)

def check_address(address, G):
    # Create an object from the Nominatim library that can convert addresses to lat and lng
    geoGuesser = Nominatim(user_agent="DSAGroup64")
    # Convert the passed-in address to lat and lng
    location = geoGuesser.geocode(address)
    # If this was successful; that is, if the address is real and can be converted into coordinates
    if location:
        # Check to see that the coordinates are within the city's general bounding box
        # City bounding box based on online resources
        if 48.812103 < location.latitude < 48.904695 and 2.246475 < location.longitude < 2.422256:
            # If the location is in bounds, find the node nearest it and return it
            node = ox.distance.nearest_nodes(G, location.longitude, location.latitude)
            return node
        else:
            # If the location is out of bounds, return nothing
            return None
    # If the conversion to coordinates did not work, return nothing
    else:
        return None

def dfs_shortest_path(G, startNode_id, endNode_id):
    # Initialize a stack for DFS
    toVisit = []
    # Keep track of visited nodes
    visited = set()
    # Empty dict of nodes and their parents
    parents = {}
    toVisit.append(startNode_id)
    visited.add(startNode_id)

    # DFS algorithm
    while toVisit: # Continues loop until the stack is empty
        # Let's get the current node's ID
        currNode = toVisit.pop()
        # If this is the node we want, break out of DFS
        if currNode == endNode_id:
            break
        # Else explore neighbors of the current node
        for neighbor in G.neighbors(currNode):
            # Checks if the neighbor has not been visited
            if neighbor not in visited:
                # Grab the information about the edge between currNode and neighbors
                edge_data = G.get_edge_data(currNode, neighbor)
                single_edge_data = list(edge_data.values())[0]
                edge_id = single_edge_data['osmid']
                edge_length = single_edge_data['length']
                toVisit.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = (currNode, edge_id, edge_length)

    # If we did the traversal and never reached the endNode, return None
    if currNode != endNode_id:
        return None
    # If we did find it
    else:
        total_length = 0
        # Iterate through the parents dict to retrace the path
        while currNode != startNode_id:
            # Add the length of the edge used to reach currNode
            total_length += parents[currNode][2]
            currNode = parents[currNode][0]
        return total_length, parents


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
    while toVisit: # Continues loop until the queue is empty
        # Let's get the current node's ID
        currNode = toVisit.pop(0)
        # If this is the node we want, break out of BFS
        if currNode == endNode_id:
            break
        # Else explore neighbors of the current node
        for neighbor in G.neighbors(currNode):
            # Checks if the neighbor has not been visited
            if neighbor not in visited:
                # Grab the information about the edge between currNode and neighbors
                edge_data = G.get_edge_data(currNode, neighbor)
                single_edge_data = list(edge_data.values())[0]
                edge_id = single_edge_data['osmid']
                edge_length = single_edge_data['length']
                toVisit.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = (currNode, edge_id, edge_length)

    # If we did the traversal and never reached the endNode, return None
    if currNode != endNode_id:
        return None
    # If we did find it
    else:
        total_length = 0
        # Iterate through the parents dict to retrace the path
        while currNode != startNode_id:
            # Add the length of the edge used to reach currNode
            total_length += parents[currNode][2]
            currNode = parents[currNode][0]
        return total_length, parents

# Define A* Search function
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
                # For each edge in the dict of edges
                for edge in edge_data:
                    # Extract the length of the edge.
                    # Using list makes the dict convert into a list we can iterate without knowing the edge IDs
                    # Index [edge] finds the current dict we want, and then ['length'] gets this edge's length
                    edge_length = list(edge_data.values())[0]['length']
                    if node_scores[currNode][1] + edge_length < node_scores[neighbor][1]:
                        node_scores[neighbor][1] = node_scores[currNode][1] + edge_length
                        # Does the same thing as getting the length above
                        edge_id = list(edge_data.values())[0]['osmid']
                        parents[neighbor] = (currNode, edge_id)
                        node_scores[neighbor][0] = node_scores[neighbor][1] + node_scores[neighbor][2]
                        visited.add(neighbor)
                        # Mark the visited node with a different color
                        G.nodes[neighbor]['color'] = 'g'
                        to_visit.put((node_scores[neighbor][0], neighbor))

    # Now we've exited, meaning that currNode is now the endNode
    totalWeight = node_scores[currNode][1]
    return totalWeight, parents

def main():
    while True:
        address = input("Enter a starting address: ")
        startNode = check_address(address, G)
        if startNode:
            print("Sounds good!")
            break
        else:
            print("Sorry, that address either doesn't exist, or it isn't in Paris. Rerun!")
    while True:
        address = input("Enter a destination address: ")
        endNode = check_address(address, G)
        if endNode:
            print("Sounds good!")
            break
        else:
            print("Sorry, that address either doesn't exist, or it isn't in Gainesville. Rerun!")

    # Draw the graph for them, blank!
    node_sizes = {startNode: 15, endNode: 15}


    # Set size 0 for all other nodes
    for node in G.nodes():
        if node not in node_sizes:
            node_sizes[node] = 0

    ox.plot_graph(G, node_size=[node_sizes[node] for node in G.nodes()])
    print("Here is a blank map depicting your start and end locations.")

    # Ask the user to choose the algorithm
    algorithm = input("Choose an algorithm (A*, BFS, or DFS): ").upper()

    if algorithm == "A*":
        shortest_path_result = a_star_search(startNode, endNode, G)
    elif algorithm == "BFS":
        shortest_path_result = bfs_shortest_path(G, startNode, endNode)
    elif algorithm == "DFS":
        shortest_path_result = dfs_shortest_path(G, startNode, endNode)
    else:
        print("Invalid algorithm choice. Please choose either A*, BFS, or DFS.")
        sys.exit()

    if shortest_path_result:
        shortest_path_length, shortest_path_parents = shortest_path_result
        print(f"Shortest path length: {shortest_path_length:.2f} meters.")

        # Extract the shortest path from the parents dictionary
        shortest_path = []
        curr_node = endNode
        while curr_node != startNode:
            shortest_path.append(curr_node)
            curr_node = shortest_path_parents[curr_node][0]
        shortest_path.append(startNode)
        shortest_path.reverse()

        print("Would you like to see nodes visited or route taken (nodes visited or route taken): ", end="")
        user_input = input().strip()

        if user_input == "route taken":
            # Plot the graph with colored nodes and the shortest path
            node_sizes = {startNode: 15, endNode: 15}
            for node in G.nodes():
                if node not in node_sizes:
                    node_sizes[node] = 0

            ox.plot.plot_graph_route(G, node_size=[node_sizes[node] for node in G.nodes()], route=shortest_path, show=True, save=True, filepath='street_map.png')
        elif user_input == "nodes visited":
            # Plot the graph with colored nodes, highlighting visited nodes in green and others in blue
            visited_nodes = set(shortest_path_parents.keys())
            node_colors = ['g' if node in visited_nodes else 'b' for node in G.nodes()]
            ox.plot.plot_graph(G, node_color=node_colors, filepath='street_map.png')
        else:
            print("Invalid Input")
            sys.exit()

    else:
        print("No path found.")

if __name__ == "__main__":
    main()