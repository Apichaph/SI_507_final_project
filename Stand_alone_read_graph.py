from Apichaph_01_retrieve_API import open_cache, save_cache # Import open_cache, save_cache from another module
from Apichaph_04_game_graph import Vertex, Graph

Steam_graph_to_store = open_cache('Steam_graph_to_store.json') # Open the graph cache
Steam_graph = Graph() # Create an empty graph object

for gamename, dict_weight in Steam_graph_to_store.items(): 
# gamename(key) is a name of game, dict_weight(value) 
# is a dictionary having another game name as a key and value as a weight
    Steam_graph.vertList[gamename] = Vertex(gamename) 
    # Assign a key in Steam_graph vertList to be a game name and value to be a vertex object with ID=key
    Steam_graph.vertList[gamename].connectedTo = dict_weight
    # For the vertex object, assign dict_weight to be connectedTo attribute

Steam_graph.numVertices = len(Steam_graph.vertList) 
# The number of vertexes in the graph equals to the number of vertList keys 

# Steam_graph is the same graph object as generated in 'Apichaph_04_game_graph.py'

#----------------------------------------------------------------------------------------------------------------#
# Checking part
print(Steam_graph.numVertices) # There are 7727 vertexes in this graph which equals to the number of games in this project
print(Steam_graph.vertList["Call of Duty 2 (2630)"].connectedTo)
# The result is {"Garry's Mod (4000)": 1, 'Grand Theft Auto III (12100)': 2, 
# 'Grand Theft Auto III (12230)': 2, 'Grand Theft Auto: San Andreas (12120)': 2,.......}
# which is the same result as in graph object generated in 'Apichaph_04_game_graph.py'

