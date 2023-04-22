from Apichaph_01_retrieve_API import open_cache, save_cache # Import open_cache, save_cache from another module

Steam_data = open_cache('Game_owned_cache.json') # Open the cache storing data users
# Data structure of Steam_data is
# {unique SteamID which is a str:
#          {"game_count": integer,
#           "games": [
#                       {"appid": int, "name": str, "playtime_forever": int, ...}, ...
#                    ]
#          }, ...
# }

Cleaned_data_cache = {} # Assign an empty dictionary

for SteamID, value in Steam_data.items(): # For each user
    if not value["game_count"] == 0: # If the user owned at least 1 game
        Cleaned_data_cache[SteamID] = [] # Assign a SteamID as a key and an empty list as a value
        for game in value['games']: # For each game that this user owned
            keep_data = {} # Assign an empty dictionary and choose specific keys that I want to use in the project
            keep_data['appid'] = str(game['appid']) # Change appid from int to str and keep in the dictionary
            keep_data['name'] = game['name'] # Keep a game name
            keep_data['playtime_forever'] = game['playtime_forever'] # Keep a playtime forever data
            Cleaned_data_cache[SteamID].append(keep_data) # Append a dictionary to the list 

# Data structure of Cleaned_data_cache is
# {unique SteamID which is a str:
#           [
#               {"appid": str, "name": str, "playtime_forever": int}, ...
#           ], ...
# }


save_cache('Cleaned_data_cache.json', Cleaned_data_cache) # Aave Cleaned_data_cache in a local cache
print(len(Cleaned_data_cache)) # As a result, there are 1148 that I can use in this project