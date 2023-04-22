from Apichaph_01_retrieve_API import open_cache, save_cache # Import open_cache, save_cache from another module

# Next, I want to create a network to reach the 1st goal of my project;
# to determine common games that users own together e.g. Dota 2 and Pub-G (will call it as a game combination)
# and ranking base on how many users own this game combination

# First I create 2 classes.
# The first class is Vertex
class Vertex:
    """
    a vertex (node) which will be used in the graph
    Class Attributes :
        id : a string
        connectedTo : a list storing neighbors of this node
    """
    def __init__(self, key): # Taking key as a parameter
        self.id = key # Assign an attribute id to a key
        self.connectedTo = {} # Assign an empty list to store which nodes they are connected to
    def addNeighbor(self, nbr): # Define a function to add a neighbor of the node
        if nbr not in self.connectedTo.keys(): # If nbr is not connected to the vertex
            self.connectedTo[nbr] = 1 # Connected to nbr and give a wight of 1
        else: # If nbr is connected to the vertex
            self.connectedTo[nbr] += 1 # Increase the weight by 1
        return self.connectedTo

# the second class is Graph
class Graph:
    """
    a graph
    Class Attributes :
        vertList : a dictionary that has a key as a vertex ID and a value as a vertex object
        numVertices : an integer represents how many nodes in the graph
    """
    def __init__(self):
        self.vertList = {} # Assign an attribute vertList to an empty dictionary
        self.numVertices = 0 # Assign an attribute numVertices as 0
    def addVertex(self, key): # Assign a function to add a node into a graph
        if key not in self.vertList.keys():
            self.numVertices += 1 # The number of nodes in the graph increases by 1
            new_vertex = Vertex(key) # A new vertex is an object in class Vertex
            self.vertList[key] = new_vertex # Store an object into a vertList dictionary as a value, using key as a key of dictionary
            # Note that key will become a vertex ID
            return new_vertex
    def addEdge(self, head, tail): # Define a function to add an edge between 2 vertices
        if head not in self.vertList: # Check if there is any vertex having the same ID as head
            new_vertax = self.addVertex(head) # If not crate a new vertex which has an ID as head
        if tail not in self.vertList: # Check if there is any vertex having the same ID as tail
            new_vertax2 = self.addVertex(tail) # If not crate a new vertex which has an ID as tail

        self.vertList[head].addNeighbor(tail) # Add vertex tail into a neighbor list (connectedTo list) of head
        self.vertList[tail].addNeighbor(head) # Add vertex head into a neighbor list (connectedTo list) of tail
    def __contains__(self, key): # Define a magic method __contain__ in order to allow checking if key in self.vertList or not
        return key in self.vertList
    def __iter__(self): # Define a magic function to allow iterable in this class
        return iter(self.vertList.values())

def main():
    # Next, I used user data to create an undirected network of games
    # Each node is a game and each edge shows how many users own the head and tail games

    # First, I opened the cache storing cleaned data users
    records = open_cache('Cleaned_data_cache.json') # Open the cache storing cleaned data users
    # Data structure of records (Cleaned_data_cache) is
    # {unique SteamID which is a str:
    #           [
    #               {"appid": str, "name": str, "playtime_forever": int}, ...
    #           ], ...
    # }

    # Second, I create a Graph object
    Steam_graph = Graph()

    # Next, I need to create nodes and add edge between nodes
    for SteamID, value in records.items(): # For each user
        owned_game = [] # Create an empty list
        for game in value: # For each game in value
            owned_game.append(f"{game['name']} ({game['appid']})") # Append the list by "game name (game ID)"

        # For example;
        # Now the owned_game will look like ['A', 'B', 'C', 'D' ]
        # Since this user have these 4 games, I added the edge between these 4 games
        # There are 4*3/2 = 6 edges in this example 
        # (4=possible head game, 3=possible tail game 
        # since this is an undirected graph, being a head or tail game is not different (A & B = B & A)
        # I have to divide by 2)
        for i in range(len(owned_game)-1) : # This will be an index for a head game
            j=i+1 # This will be an index for a tail game
            while j<len(owned_game): # Keep looping as long I don't run out of tail game to loop
                Steam_graph.addEdge(owned_game[i], owned_game[j]) # Add an edge between these 2 games
                j += 1 # Then, continue for the next tail game

        # Continue from an example above, len(owned_game) = 4 and len(owned_game))-1 = 3
        # i = 0, j = 1 since j<len(owned_game), I add edge between 'A' & 'B'
        # i = 0, j = 2 since j<len(owned_game), I add edge between 'A' & 'C'
        # i = 0, j = 3 since j<len(owned_game), I add edge between 'A' & 'D'
        # Now, j = 4, I stop inner looping and move on to the next i
        # i = 1, j = 2 since j<len(owned_game), I add edge between 'B' & 'C'
        # i = 1, j = 3 since j<len(owned_game), I add edge between 'B' & 'D'
        # Now, j = 4, I stop inner looping and move on to the next i
        # i = 2, j = 3 since j<len(owned_game), I add edge between 'C' & 'D'
        # Now, j = 4, I stop inner looping and have 6 combinations

    print(Steam_graph.numVertices) 
    # There are 7727 vertexes in this graph which equals to the number of games in this project
    print(Steam_graph.vertList["Call of Duty 2 (2630)"].connectedTo)
    # To check that the vertex of game connecting to other games, I choose "Call of Duty 2 (2630)" 
    # to see if it is connected to any neighbors.
    # The result is {"Garry's Mod (4000)": 1, 'Grand Theft Auto III (12100)': 2, 
    # 'Grand Theft Auto III (12230)': 2, 'Grand Theft Auto: San Andreas (12120)': 2,.......}

    # I make another dictionary to show the structure of the graph. Since the original value of Steam_graph.vertList
    # is an object vertex, I used an attribute connectedTo to show the neighbors of the key vertex.
    Steam_graph_to_store = {key:value.connectedTo for key, value in Steam_graph.vertList.items()}
    save_cache('Steam_graph_to_store.json', Steam_graph_to_store) # save cache

    #--------------------------------------------------------------------------------------------------------------#

    # The next step is to transform a data in the graph into a proper-to-use structure
    # Due to the network structure, e.g. the vertex 'A' will have 'X' as a neighbor with a weight 'M'
    # and the vertex 'X' will have 'A' as a neighbor with a weight 'M'
    # Since 'A' & 'X' and 'X' & 'A' have the same message (How many users own the game 'A' and 'X'),
    # I only need to store one of them.

    game_combinations = {} # Create an empty dictionary
    # I will store a name that represents a combination as a key and how many users own this combination as a value
    for appid, vertex in Steam_graph.vertList.items(): # Key is game ID and value is a vertex object
        for neighbor, weight in vertex.connectedTo.items():
            # For each vertex, access a dictionary that contains neighbors (which is a "game name (game ID)") and weight
            combination_key = f"{appid} & {neighbor}" # This is a name of the key I want to store in game_combinations dictionary
            reverse_combination_key = f"{neighbor} & {appid}" # This is a reverse key
            if combination_key in game_combinations.keys() or reverse_combination_key in game_combinations.keys():
                # If the combination is already stored in the dictionary, continue to the next neighbor
                # e.g. If I already store 'A' & 'X' and I found 'X' & 'A', I will ignore it
                continue
            else: # If the combination is not stored in the dictionary yet
                game_combinations[combination_key] = weight # Store the combination name as a key and a weight as a value

    game_combinations = dict(sorted(game_combinations.items(), key= lambda x:x[1], reverse=True)) 
    # Sort by weight value from the highest to lowest
    # Data structure of game_combinations is
    # [{combination name which is a string: weight which is an int},...]

    # Next, I want to rank the game combination
    # I find the highest weight
    highest_count = max(game_combinations.values()) # 359

    ranking_combination = [] # Create an empty list
    i = 0 # Start from 0

    while len(ranking_combination) < len(game_combinations):
        # Keep looping until the number of combination in ranking_combination and game_combinations are equal
        rank = len(ranking_combination)+1
        # Assign a rank number, e.g. if there are 2 games in the ranking_combination, the next rank should be 3
        for combination_name, count in game_combinations.items(): # For each combination
            if count == highest_count-i:
                # If a game count equal to this number, append the list by a dictionary containing related data of this game
                ranking_combination.append({'rank': rank, 'name': combination_name, 'count': count,})
        i += 1  # Increase i by 1

    save_cache('ranking_combination.json', ranking_combination) # Save the cache

    print(len(ranking_combination)) # There are 4602216 game combinations in my project
if  __name__ == "__main__":
    main()

