import datetime
import requests
import json
import random
import time
# from API_key import APIkey # I already revoke my API

def get_the_info(APIkey, SteamID):
    '''
    Using API to retrieve games owned by a Steam user.
    Parameter :
        Key : a sequence of integers and alphabets represent API key
        SteamID : a sequence of 17-digit unique identifier for each user on Steam
    Peturn :
        dictionary : a dictionary consist of 2 keys
                    1) "game_count" shows how many games this person owned
                    2) "games" shows a list of games this person owned
    '''
    response = requests.get(
        f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={APIkey}&steamid={SteamID}&format=json&include_played_free_games=True&include_appinfo=True"
        ) # Retrieve the API data from Steam
    if response.status_code == 200: # If the request has succeeded. In other words, if this Steam ID exists.
        # If the Steam ID is public, the structure of the key - value is
        # {"response": {"game_count": integer, "games": [{"appid":integer, "playtime_forever":integer, "name":str, .....},.....]}}
        # If the Steam ID is private , the structure of the value is {}
        # {"response":{}}
        response_object = json.loads(response.text) # Transform into a dictionary structure
        return response_object['response'] # Return the value of the key response

    else: # If the request is something else
        return {} # return an empty dictionary

def open_cache(Cache_filename):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters :
        Cache_filename : name of cache file that wants to open

    Returns
    -------
        dictionary : the opened cache
    '''
    try:
        cache_file = open(Cache_filename, 'r') # Open json file with a read mode
        cache_contents = cache_file.read() # Read a json file
        cache_dict = json.loads(cache_contents) # Transform json into dictionary
        cache_file.close() # Close the file
    except:
        cache_dict = {} # If there is no Cache_filename, generate an empty dictionary
    return cache_dict

def save_cache(Cache_filename, cache_dict):
    ''' saves the current state of the cache to disk
    Parameters :
        Cache_filename : name of cache file that wants to save the cache_dict
        cache_dict: dictionary that wants to save

    Returns :
        None
    '''
    dumped_json_cache = json.dumps(cache_dict) # Transform cache_dict into json format
    fw = open(Cache_filename,"w") # Open CACHE_FILENAME with a write mode
    fw.write(dumped_json_cache) # Write cache_dict(json format) in CACHE_FILENAME
    fw.close() # Close the file

def random_ID():
    ''' generate random Steam ID which is a 17-digit code
    the first 7 digits are 7656119 because, base of my research, all valid Steam ID start with these 7 digits
    the next digit randomly choose between 7,8,9 to increase the probability of obtaining a valid Steam ID
    Parameters :
        None
    
    Returns :
        SteamID : a string of 17 digits
    '''
    SteamID = '7656119' # fix the first 7 digits
    SteamID = SteamID + str(random.randint(7,9)) # randomly choose the next digit from 7,8,9
    for i in range(9): # for the next 8 digits,
        newdigit = str(random.randint(0,9)) # each position randomly chooses from 0 to 9
        SteamID = SteamID + newdigit # merge all the 17 digits together
    return SteamID

def main():
    """Entry point for the script.
    Paramters:
        None
    Returns:
        None
    """

    # I have two cache files to retrieve the API data
    # 1) SteamID_cache : a dictionary with 2 keys
            # "valid_ID" has the value of the list containing all the existing and public Steam ID
            # "invalid_ID" has the value of the list containing all the non-existing or private Steam ID
    # 2) Game_owned_cache : a dictionary with a Steam ID as a key and the retrieved data for that ID as a value

    # One of the pros of SteamID_cache is that I can see the pattern of stream ID, and adjust random_ID() to scope 
    # some positions to increase the probability of obtaining a valid Steam ID

    # Open the cache
    SteamID_cache = open_cache('SteamID_cache.json')
    Game_owned_cache = open_cache('Game_owned_cache.json')

    # My constrains are 1) Steam limits 100,000 calls per day
    # 2) If too many calls are made too quickly, I will get kick out from the system
    # Thus, I have been coded in several ways to find the best method for me to retrieve API
    # And the method I choose is as followed

    calls = int(input("How many calls I want to retrieve API: "))
    # I can retrieve a several calls if I have limited time or I can retrieve a thousand calls if I have enough time

    for i in range(calls):
        steamID = random_ID() # Generate a random Steam ID
        if steamID in SteamID_cache['invalid_ID'] or steamID in SteamID_cache['valid_ID']: # If this Steam ID has already used before
            continue # continue to the next Steam ID
        else: # If this Steam ID has never been used to retrieve data before
            dict_return = get_the_info(APIkey, steamID) # Retrieve API data
            if dict_return == {}:
                # If the request has not succeeded or the request has succeeded but the ID is not public.
                # Both cases return an empty dictionary
                SteamID_cache['invalid_ID'].append(steamID) # store an ID in SteamID_cache with the key invalid_ID
            else: # If the request has succeeded and the ID is public
                SteamID_cache['valid_ID'].append(steamID) # store an ID in SteamID_cache with the key valid_ID
                # So, I assign a new key in the dictionary getting from API to store the time
                Game_owned_cache[steamID] = dict_return 
                # Store the data into the dictionary Game_owned_cache as a value which will be saved as a cache
                # A key is the Steam ID
                print(len(Game_owned_cache.keys())) # Checking how many data I have

        save_cache('SteamID_cache.json', SteamID_cache) # Save SteamID_cache in to a local cache
        save_cache('Game_owned_cache.json', Game_owned_cache) # Save Game_owned_cache in to a local cache
        time.sleep(0.5) # To prevent kicking out from retrieving API


if __name__ == "__main__":
    main()
