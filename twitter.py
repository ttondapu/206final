import requests
from bs4 import BeautifulSoup as bs
import json
import os
import matplotlib
import sqlite3
import matplotlib.pyplot as plt

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIRqbwEAAAAA4bw%2B4KetqBn%2BP57DDgFOKCZN6Qs%3DQJGvijx8WwBq28D4pUOZ2ZLMHicJe7g4A3cJGiKs9wDWigyQM0'

def createDB(filename):
    '''
    This function initializes the database (if not already created) to be used throughout this project.
    filename.db will be found in the current working directory. 
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def setUpTwitterTable(favartists, cur, conn):
    '''
    This function takes in a list of artists and a cur/conn pointing to a database. 
    When run, it will populate the twitter table inside the database, inserting an entry for each 
    artist inclduing information about their username, number of followers, and number of tweets.
    '''
    cur.execute('DROP TABLE IF EXISTS twitter')
    cur.execute('CREATE TABLE twitter (artist_id INTEGER UNIQUE PRIMARY KEY, twitter_handle TEXT, follower_count INTEGER, tweet_count INETEGER)')
    counter = 0
    for i in favartists.keys():
        print(i)
        url = create_url(favartists[i])
        data = get_artist_info(url)
        if favartists[i] != '0':
            twitter_handle = data[0]
            follower_count = data[1]
            tweet_count = data[2]
            artist_id = counter
            cur.execute("INSERT OR IGNORE INTO twitter (artist_id, twitter_handle, follower_count, tweet_count) VALUES (?,?,?,?)", (artist_id, twitter_handle, follower_count, tweet_count))
            counter += 1
    conn.commit()

def create_url(user_id):
    '''
    This function takes in a twitter user id and returns a url to access their account from the API.
    '''
    return "https://api.twitter.com/2/users/{}?user.fields=public_metrics".format(user_id)

def bearer_oauth(r):
    """
    DO NOT EDIT: This function is from the twitter dev site to authorize our program.
    It utilizes the bearer token found at the top.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowerLookupPython"
    return r

def get_artist_info(url):
    '''
    This function takes a twitter api url and returns the json response object.
    '''
    response = requests.request("GET", url, auth=bearer_oauth, params={})
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
    json_response = response.json()
    return((json_response['data']['username'], json_response['data']['public_metrics']['followers_count'], json_response['data']['public_metrics']['tweet_count']))

def main():
    favartists = {'Ed Sheeran' : '85452649',
    'The Weeknd' : '255388236',  
    'Billie Eilish'	: '2150327072',
    'Justin Bieber' : '27260086',
    'Taylor Swift' : '17919972',
    'Drake' : '27195114',
    'Eminem' : '22940219',
    'Post Malone' : '913812620',
    'Kanye West' : '169686021',
    'Juice Wrld' :'3676932858'}

    cur, conn = createDB('finalproj.db')
    setUpTwitterTable(favartists, cur, conn)

main()