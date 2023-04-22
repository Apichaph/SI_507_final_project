from flask import Flask, render_template, request
from Apichaph_01_retrieve_API import open_cache, save_cache # import cache functions from another module
import requests
import json
import datetime

# Define a function to make an API call and choose a key-value pair to display to the web-user
def get_latest_news(appid):
    try:
        response = requests.get(
            f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count=50&maxlength=500&format=json"
            ).json() # Make an API call and convert to dictionary format
        # The structure of response is 
        # {"appnews":{"appid":{gameID},"newsitems":[{"title":___,"url":___,"date":___,...}, ...another news...]}
        response = response["appnews"]["newsitems"] # Choose the key appnews and newsitems

        news = [] # Create an empty list
        for new in response: 
            news.append({'title': new["title"], 'url': new['url'], \
                        'date': datetime.datetime.fromtimestamp(new['date']).strftime("%Y-%m-%d")})
            # Choose only title, url, and convert date from unix timestamp to year-month-date format
        return news # return the list
    except:
        return [] # return empty list
    
# There are 8 routes in this project
# 1) homepage
# 2) showing a game rank base on how many Steam users own this game
# 3) showing a game rank base on how long Steam users have been dedicated to this game
# 4) showing a game combination rank base on how many users own this combination
# 5 and 6) User can search ranks by game name or game ID to see the ranks of that game or
# can search by rank to see what games are on this rank
# 7) checking a game name or game ID whether this game is in the project or not
# 8) showing the latest 50 news of a specific game

# Flask part
app = Flask(__name__)

game_id_name = open_cache('game_id_name.json')
ranking_owned_game = open_cache('ranking_owned_game.json') # Open the cache
ranking_duration_game = open_cache('ranking_duration_game.json') # Open the cache
ranking_combination = open_cache('ranking_combination.json') # Open the cache

# Page 1) homepage
@app.route("/")
def home():
    return render_template('homepage.html')

# Page 2) rank by how many Steam user own the games
@app.route("/rankbyownership")
def rankbyownership():
    return render_template('ownership.html', ranking_owned_game=ranking_owned_game)

# Page 3) rank by how long Steam users have been dedicated to this game
@app.route("/rankbyduration")
def rankbyduration():
    return render_template('duration.html', ranking_duration_game=ranking_duration_game)

# Page 4) a game combination rank base on how many users own this combination
@app.route("/popularcombination")
def popularcombination():
    return render_template('combination.html', ranking_combination=ranking_combination)

# Page 5) web user can search for ranks of specific games or games for specific rank (individual game rank)
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            query = request.form['query']
        except:
            query = ''

        try:
            rankinput = int(request.form['rankinput'])
        except:
            rankinput = ''

        return render_template('search.html', query=query, rankinput=rankinput,
                               ranking_owned_game=ranking_owned_game,
                               ranking_duration_game=ranking_duration_game,
                               ranking_combination=ranking_combination)
    else:
        return render_template('search.html',
                               ranking_owned_game=ranking_owned_game,
                               ranking_duration_game=ranking_duration_game,
                               ranking_combination=ranking_combination)
        
# Page 6) web user can search for ranks of specific games or games for specific rank (game combination rank)
@app.route('/search_combination', methods=['GET', 'POST'])
def search_combination():
    if request.method == 'POST':
        try:
            query = request.form['query']
        except:
            query = ''

        try:
            rankinput = int(request.form['rankinput'])
        except:
            rankinput = ''

        return render_template('search_combination.html', query=query, rankinput=rankinput,
                               ranking_owned_game=ranking_owned_game,
                               ranking_duration_game=ranking_duration_game,
                               ranking_combination=ranking_combination)
    else:
        return render_template('search_combination.html',
                               ranking_owned_game=ranking_owned_game,
                               ranking_duration_game=ranking_duration_game,
                               ranking_combination=ranking_combination)

# Page 7) convert a game name into game ID or vice versa
@app.route("/gameid_gamename",  methods=['GET', 'POST'])
def gameid_gamename():
    if request.method == 'POST':
        try:
            nameinput = request.form['nameinput']
        except:
            nameinput = ''

        try:
            idinput = request.form['idinput']
        except:
            idinput = ''

        return render_template('gameid_gamename.html', nameinput=nameinput, idinput=idinput,
                               game_id_name=game_id_name)

    else:
        return render_template('gameid_gamename.html', game_id_name=game_id_name)

# Page 8) showing 50 latest news of specific games
@app.route("/news",  methods=['GET', 'POST'])
def news():
    if request.method == 'POST':
        newsinput = request.form['newsinput']
        try:
            newsinput= int(newsinput)
            news_list = get_latest_news(int(newsinput))
        except:
            news_list = []
        return render_template('news.html', newsinput=newsinput, news_list=news_list)
    else:
        return render_template('news.html')
    
if __name__=='__main__':
    app.run(debug=True) # Using debug=True to help debugging process more conveniently