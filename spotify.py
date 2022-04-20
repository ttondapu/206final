import requests
from bs4 import BeautifulSoup as bs
import json
import os
import matplotlib
import sqlite3
import matplotlib.pyplot as plt

def createDB(filename):
    '''
    initializes database
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def artistalbumsurl(id):
    '''
    generates a url to access an artist's discography
    '''
    return "https://api.spotify.com/v1/artists/" + id + "/albums"

def albumurl(id):
    '''
    generates a url to access a specific album
    '''
    return "https://api.spotify.com/v1/albums/" + id

def get_artist_albums(artistid, offset, cur): 
    '''
    just a test function to familiarize myself with spotify's API,
    returns a list of information about each of an artist's albums
    '''
    #must update token every time :/ go to https://developer.spotify.com/console/get-album/
    token = 'BQBbCpsLEy0Z1jAwxsJkSIWytwQvO4mHQMp8L5U9P_V01Wea6jZAfmUREVzQ1QvMjHTcX7nyFrt9AwK2IV0m2TMhw8KT98pKc2Mkl9YUDspXXcPAcXROD447f6fisnMOdPvR5ckdSXDuQsmw6KrMxOc1V50xu1ejGdw'
    url = artistalbumsurl(artistid)
    param = {'limit': 25,'offset': offset, 'access_token': token}
    response = requests.get(url, params = param)
    results = response.json()
    albumids = []
    for x in results['items']:
        albumids.append(x['id'])
    data = []
    for y in albumids:
        url = albumurl(y)
        param = {'access_token' : token}
        response = requests.get(url, params = param)
        results = response.json()
        title = results['name']
        date = results['release_date']
        totaltracks = int(results['total_tracks'])
        #feel free to add whatever data u want to gather here
        #https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-album
        #list of possible keys ^
        if totaltracks > 3: #to ensure we aren't including singles as albums
            data.append((title, date))
    return data

def main():
    '''
    putting it all together
    '''
    favartists = {'Lil Uzi Vert' : '4O15NlyKLIASxsJ0PrXPfz',
        'Olivia Rodrigo' : '1McMsnEElThX1knmY4oliG', 
        'Ed Sheeran' : "6eUKZXaKkcviH0Ku9w2n3V",
        'Post Malone' : '246dkjvS1zLTtiykXe5h60',
        'The Weeknd' : '1Xyo4u8uXC1ZmMpatF05PJ',
        'Ariana Grande' : '66CXWjxzNUsdJxJ2JdwvnR',
        'Justin Bieber' : '1uNFoZAHBGtllmzznpCI3s'}

    cur, conn = createDB('spotify.db')
    try:
        cur.execute('SELECT name FROM spotify_results WHERE name  = Lil Uzi Vert')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0
    data = get_artist_albums(favartists['Olivia Rodrigo'], start, cur)
    print(data) #to see if the api is working

main()
