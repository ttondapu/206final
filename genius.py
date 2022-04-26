import requests
from bs4 import BeautifulSoup as bs
import json
import os
import matplotlib
import sqlite3
import matplotlib.pyplot as plt
from sqlalchemy import all_


# constants

BASE_URL = "https://api.genius.com"
TOKEN = "GXbwC9RH0ntDv_KvahB_M7iVeqxQN4d0oruo68Da2kE2wFtj-kX96U5Rux_b9rvs"
ARTIST_NAMES = ['Ed Sheeran', 'The Weeknd', 'Billie Eilish', 'Justin Bieber', 'Taylor Swift', 'Drake', 'Eminem', 'Post Malone', 'Kanye West', "Juice WRLD"]
# ARTIST_NAMES = ['Juice Wrld']


def createDB(filename):
    '''
    This function initializes the database (if not already created) to be used throughout this project.
    filename.db will be found in the current working directory.
    '''

    # print("createDB")

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + filename)
    cur = conn.cursor()

    return cur, conn


def setUpGeniusTable(ARTIST_NAMES, cur, conn):
    '''
    This function takes in a list of artists and a database cur/conn.
    It then creates a table inside the database pointed to by cur/conn with an artist's information
    which includes the artist id, name, and Genius followers.
    '''

    # print("setUpGeniusTable")

    cur.execute('DROP TABLE IF EXISTS genius_artists')
    cur.execute('CREATE TABLE genius_artists (id INTEGER UNIQUE PRIMARY KEY, artist_name TEXT, follower_count INTEGER)')
    
    for i, artist in enumerate(ARTIST_NAMES):
        id = i 
        artist_id = get_id(artist)
        # song_ids = get_artist_song_ids(artist_id)
        # full_list_of_songs = get_song_names(song_ids)
        follower_count = get_artist_followers(artist_id)
        cur.execute("INSERT OR IGNORE INTO genius_artists (id, artist_name, follower_count) VALUES (?, ?, ?)", (id, artist, follower_count))

    conn.commit()

def setUpGeniusTable2(ARTIST_NAMES, cur, conn):
    '''
    This function takes in a list of artists and a database cur/conn.
    It then creates a table inside the database pointed to by cur/conn with an artist's information
    which includes the artist id, name, and Genius followers.
    '''

    # print("setUpGeniusTable2")

    cur.execute('DROP TABLE IF EXISTS genius_songs')
    cur.execute('CREATE TABLE genius_songs (id INTEGER UNIQUE PRIMARY KEY, song INTEGER)')
    
    id = 0

    for artist in ARTIST_NAMES:
        artist_id = get_id(artist)
        song_ids = get_artist_song_ids(artist_id)
        full_list_of_songs = get_song_names(song_ids)
        # follower_count = get_artist_followers(artist_id)
        for songs in full_list_of_songs.values():
            for song in songs:
                print(song)
                cur.execute("INSERT OR IGNORE INTO genius_songs (id, song) VALUES (?, ?)", (id, song))
                id += 1
                print(id)

    conn.commit()


def start(path, params = None, headers = None):
    '''
    This function sends a request for a url and gets json data from that url.
    It requires a token, hard coded at the beginning of the code.
    '''

    # print("start")

    url = BASE_URL + "/" + path
    token = "Bearer " + TOKEN
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}

    response = requests.get(url = url, params = params, headers = headers)
    response.raise_for_status()

    return response.json()


def get_id(artist_name):
    '''
    This function takes in an artist's name from the list and returns their id.
    '''

    # print("get_id")
    
    find_id = start("search", {'q': artist_name})
    for a in find_id["response"]["hits"]:
        if a["result"]["primary_artist"]["name"] == artist_name:
            artist_id = a["result"]["primary_artist"]["id"]
            break

    return artist_id


def get_artist_song_ids(artist_id):
    '''
    This function iterates through each page and returns a list of the artist's songs' ids excluding songs they are only featured on. 
    '''

    # print("get_artist_song_ids")

    current_page = 1
    next_page = True 
    songs = []

    while next_page:

        path = "artists/" + str(artist_id) + "/songs/"
        params = {'page': current_page}
        data = start(path = path, params = params)

        page_songs = data['response']['songs']
        
        # print(data['response'])

        if page_songs:
            songs += page_songs
            current_page += 1
        else:
            next_page = False

    songs = [song["id"] for song in songs if song["primary_artist"]["id"] == artist_id][0:10]

    print(type(songs))

    return songs


def get_song_names(song_ids):
    '''
    This function returns a dictionary of the artist's songs using their ids, which were passed in.
    '''

    # print("get_song_names")

    song_dict = {}

    for i, song_id in enumerate(song_ids):
        path = "songs/" + str(song_id)
        
        data = start(path = path)["response"]["song"]

        if data["primary_artist"]["name"] not in song_dict.keys():
            song_dict[data["primary_artist"]["name"]] = [data["title"]]
        else:
            song_dict[data["primary_artist"]["name"]] += [data["title"]]

    # print(song_lst)
    return song_dict


def get_artist_followers(artist_id):
    '''
    This function sends in the artist's id and gets the artist's followers.
    '''

    # print("get_artist_followers")
    
    path = "artists/" + str(artist_id)
    data = start(path = path)

    followers = data["response"]["artist"]["followers_count"]
    # print(data) # results all the way at bottom 
    return followers


# just added, may not work
# def get_song_date(song_ids):
#     song_lst2 = {}

#     for i, song_id in enumerate(song_ids):
#         path = "songs/" + str(song_id)
        
#         data = start(path = path)["response"]["song"]

#         if data["release_date"] not in song_lst2.keys():
#             song_lst2["release_date"] = data["release_date"]
#         else:
#             song_lst2["release_date"] = data["release_date"]

#     print(song_lst2)
#     return song_lst2


def main():

    # ARTIST_NAMES = ['Ed Sheeran', 'The Weeknd', 'Ariana Grande', 'Justin Bieber', 'Taylor Swift', 'Drake', 'Eminem', 'Post Malone', 'Kanye West', 'Juice Wrld']
    
    # for artist in ARTIST_NAMES:
    #     artist_id = get_id(artist)

    #     # get all song ids and make a list
    #     song_ids = get_artist_song_ids(artist_id)

    #     # finally, make a full list of songs names
    #     full_list_of_songs = get_song_names(song_ids)

    #     get_artist_followers(artist_id)
    
    cur, conn = createDB('finalproj.db')
    setUpGeniusTable(ARTIST_NAMES, cur, conn)
    setUpGeniusTable2(ARTIST_NAMES, cur, conn)
    #get_id(ARTIST_NAMES)

main()


# for artist in ARTIST_NAMES:

#     find_id = start("search", {'q': artist})
#     for b in find_id["response"]["hits"]:
#         if b["result"]["primary_artist"]["name"] == artist:
#             artist_id = b["result"]["primary_artist"]["id"]
#             break

    