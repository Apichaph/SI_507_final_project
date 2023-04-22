from Apichaph_01_retrieve_API import open_cache, save_cache # Import cache functions from another module

Cleaned_data_cache = open_cache('Cleaned_data_cache.json') # Open the cache storing retrieved user data
# Data structure of Cleaned_data_cache is
# {unique SteamID which is a str:
#           [
#               {"appid": str, "name": str, "playtime_forever": int}, ...
#           ], ...
# }

game_id_name = {} # Create an empty dictionary. It will use to store game ID as a key and game name as a value

for value in Cleaned_data_cache.values(): # For each list corresponding to unique user SteamID
    for game in value: # For each game in the list
        if game['appid'] not in game_id_name.keys(): # If game ID not in the game_id_to_name yet
            game_id_name[game['appid']] = game['name'] # Use game ID as a key and name as a value

save_cache('game_id_name.json', game_id_name) # Save data into a local cache
print(len(game_id_name)) # They are 7727 games in this project