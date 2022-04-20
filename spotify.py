import requests
from bs4 import BeautifulSoup as bs
import json
import os
import sys
import matplotlib
import sqlite3
import unittest
import csv
import matplotlib.pyplot as plt

def createDB(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def artistalbumsurl(id):
    #spotify:artist:4O15NlyKLIASxsJ0PrXPfz
    #spotify:track:4cOdK2wGLETKBW3PvgPWqT
    return "https://api.spotify.com/v1/artists/" + id + "/albums"

def albumurl(id):
    return "https://api.spotify.com/v1/albums/" + id

def get_artist_albums(artistid, offset, cur): 
    #must update token every time :/
    #link here https://developer.spotify.com/console/get-album/
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
            data.append((title, date, totaltracks))
    return data

def main():
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
