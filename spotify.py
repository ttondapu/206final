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

def artistalbumsurl(artistid):
    '''
    generates a url to access an artist's discography
    '''
    return "https://api.spotify.com/v1/artists/" + artistid + "/albums"

def albumurl(albumid):
    '''
    generates a url to access a specific album
    '''
    return "https://api.spotify.com/v1/albums/" + albumid

def artisturl(artistid):
    '''
    generates a url to access a specific artist
    '''
    return "https://api.spotify.com/v1/artists/" + artistid

def create_table_two(artistid, token, offset): 
    '''
    returns list of an artist's releases with number of tracks and release date
    '''
    #must update token every time :/ go to https://developer.spotify.com/console/get-album/
    tracklist = []
    url = artistalbumsurl(artistid)
    param = {'limit': 25,'offset': offset, 'access_token': token}
    response = requests.get(url, params = param)
    results = response.json()
    albumids = []
    for x in results['items']:
        albumids.append(x['id'])
    data = []
    totaltracks = 0
    for y in albumids:
        url = albumurl(y)
        param = {'access_token' : token}
        response = requests.get(url, params = param)
        results = response.json()
        tracklist.append((results['name'], results['total_tracks'], results['release_date']))
        #feel free to add whatever data u want to gather here
        #https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-album
        #list of possible keys ^
    return tracklist

def create_table_one(artistid, token, offset): 
    '''
    returns tuple of an artist's info including name, total number of tracks on albums, and number of followers
    '''
    #must update token every time :/ go to https://developer.spotify.com/console/get-album/
    url = artisturl(artistid)
    param = {'limit': 25,'offset': offset, 'access_token': token}
    response = requests.get(url, params = param)
    results = response.json()
    artistname = results['name']
    numfollowing = int(results['followers']['total'])
    url = artistalbumsurl(artistid)
    param = {'limit': 25,'offset': offset, 'access_token': token}
    response = requests.get(url, params = param)
    results = response.json()
    albumids = []
    for x in results['items']:
        albumids.append(x['id'])
    totaltracks = 0
    for y in albumids:
        url = albumurl(y)
        param = {'access_token' : token}
        response = requests.get(url, params = param)
        results = response.json()
        totaltracks += int(results['total_tracks'])
        #feel free to add whatever data u want to gather here
        #https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-album
        #list of possible keys ^
    return (artistname, numfollowing, totaltracks)

def main():
    favartists = {'Ed sheeran' : '6eUKZXaKkcviH0Ku9w2n3V',
    'The Weeknd' : '1Xyo4u8uXC1ZmMpatF05PJ',  
    'Ariana Grande'	: '66CXWjxzNUsdJxJ2JdwvnR',
    'Justin bieber' : '1uNFoZAHBGtllmzznpCI3s',
    'Taylor swift' : '06HL4z0CvFAxyc27GXpf02',
    'Drake' : '3TVXtAsR1Inumwj472S9r4',
    'Eminem' : '7dGJo4pcD2V6oG8kP0tJRR',
    'Post Malone' : '246dkjvS1zLTtiykXe5h60',
    'Kanye' : '5K4W6rqBFWDnAN6FQUkS6x',
    'Juice Wrld' :'4MCBfE4596Uoi2O4DtmEMz'}
    
    cur, conn = createDB('spotify.db')
    try:
        cur.execute('SELECT name FROM spotify_results WHERE name  = Lil Uzi Vert')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0

    token = 'BQDO6dUrWwNWoY6BZWU3VcaNFWuOGGlt0656i-pFH0LcWiRJ1DuDk4_f-qdBWFS1OUvnCj-qAEmMyTEdZEuTylss3YdML1uUItboQs-ZsmCib5aAECinoXfMT4Ms_8O3iX9_KDpI1FycPH4KjjcOVoMNcBrZfR66ML8'
    data = create_table_two(favartists['Lil Uzi Vert'], token, start)
    print(data) #to see if the api is working
    print()
    data = create_table_one(favartists['Lil Uzi Vert'], token, start)
    print(data)

main()