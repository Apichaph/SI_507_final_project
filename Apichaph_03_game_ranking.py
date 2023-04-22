from Apichaph_01_retrieve_API import open_cache, save_cache # Import open_cache, save_cache from another module

records = open_cache('Cleaned_data_cache.json') # Open the cache storing cleaned data users
# Data structure of records (Cleaned_data_cache) is
# {unique SteamID which is a str:
#           [
#               {"appid": str, "name": str, "playtime_forever": int}, ...
#           ], ...
# }

# This part aims to achieve 2 goals; 1) to determine the number of people who own this game and its ranking 
# in order to achieve the 2nd goal of the project.
# 2) to determine how long people have been playing this game and its ranking
# in order to achieve the 3rd goal of the project.

popular_owned_game = {} # Create an empty dictionary to store the number of game owner
duration_played_game = {} # Create an empty dictionary to store the duration users playing this game
for SteamID, value in records.items(): # For each user
    for game in value: # For each game that this user own

        if game['appid'] not in popular_owned_game.keys(): # If this game ID is not in popular_owned_game dictionary yet
            popular_owned_game[game['appid']] = {'count': 1, 'name': game['name']}
            # Keep a game ID as a key and another dictionary as a value.
            # A new dictionary has 2 keys, 1) an integer representing how many people own this game starting from 1
            # 2) a game name
        else: # If this game ID is already in popular_owned_game dictionary
            popular_owned_game[game['appid']]['count'] += 1 # Increase the count by 1

        if game['appid'] not in duration_played_game.keys(): # If this game ID is not in duration_played_game dictionary yet
            duration_played_game[game['appid']]  = {'playtime': int(round(game['playtime_forever']/(60*24), 0)), 'name': game['name']}
            # Keep a game ID as a key and another dictionary as a value.
            # A new dictionary has 2 keys, 1) an integer representing how long users have been playing this game (in days)
            # game['playtime_forever'] originally store in minute unit, so I divided by 60 to convert to hour unit
            # and then divided by 24 to convert to day unit. Then, I round it to a integer
            # 2) a game name
        else: # If this game ID is already in duration_played_game dictionary
            duration_played_game[game['appid']]['playtime'] += int(round(game['playtime_forever']/(60*24), 0))
            # Increase a playtime counting by how long this user playing this game

# Data structure of popular_owned_game is 
# {gameID which is a str: {"count": int, "name": str}, ...}

# Data structure of popular_owned_game is 
# {gameID which is a str: {"playtime": int, "name": str}, ...}

# ------------------------------------------------------------------------------------------------------------------ #

# Next step is to rank games based on how many uses own this game
# First I need to find the highest game count
highest_count = 0
for value in popular_owned_game.values(): # Value is {"count": int, "name": str}
    if value['count'] > highest_count: # If a count is higher than highest_count
        highest_count = value['count'] # Assign the count to be a new highest_count

print(highest_count) # As a result, a highest count is 813

ranking_owned_game = [] # Create an empty list
i = 0 # Start from 0
while len(ranking_owned_game) < len(popular_owned_game):
    # Keep looping until the number of game in ranking_owned_game and popular_owned_game are equal
    rank = len(ranking_owned_game)+1
    # Assign a rank number, e.g. if there are 2 games in the ranking_owned_game, the next rank should be 3
    for appid, value in popular_owned_game.items(): # For each game
        if value['count'] == highest_count-i:
        # If a game count equal to this number, append the list by a dictionary containing related data of this game
            ranking_owned_game.append({
                'rank': rank,
                'appid': appid,
                'name': value['name'],
                'count': value['count'],
                })
    i += 1 # Increase i by 1

save_cache('ranking_owned_game.json', ranking_owned_game)  # Save the cache
# Data structure of ranking_owned_game is
# [{"rank": int, "appid": str, "name": str, "count": int},...]

# ------------------------------------------------------------------------------------------------------------------ #

# The final step is to rank games based on how long users have been playing this game
# First I need to find the longest duration

longest_duration = 0
for value in duration_played_game.values(): # Value is {"playtime": int, "name": str}
    if value['playtime'] > longest_duration: # If a playtime is longer than longest_duration
        longest_duration = value['playtime'] # Assign the playtime to be a new longest_duration

ranking_duration_game = [] # Create an empty list
i = 0 # Start from 0
while len(ranking_duration_game) < len(duration_played_game):
    # Keep looping until the number of game in ranking_duration_game and duration_played_game are equal
    rank = len(ranking_duration_game)+1
    # Assign a rank number
    for appid, value in duration_played_game.items(): # For each game
        if value['playtime'] == longest_duration-i:
        # If a game duration equal to this number, append the list by a dictionary containing related data of this game
            ranking_duration_game.append({
                'rank': rank,
                'appid': appid,
                'name': value['name'], 
                'playtime': value['playtime'], 
                })
    i += 1 # Increase i by 1

save_cache('ranking_duration_game.json', ranking_duration_game) # Save the cache
# Data structure of ranking_duration_game is
# [{"rank": int, "appid": str, "name": str, "playtime": int}, ...]

# ------------------------------------------------------------------------------------------------------------------ #
# Checking how many games I have in this project
# And Checking that the number of games in both ranking_duration_game and ranking_owned_game are equal
print(len(ranking_duration_game)) # show 7727
print(len(ranking_owned_game)) # show 7727
print(len(ranking_duration_game) == len(ranking_owned_game)) # show True