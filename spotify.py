import requests
from bs4 import BeautifulSoup as bs
import json
import os
import matplotlib
import sqlite3
import matplotlib.pyplot as plt

def createDB(filename):
    '''
    This function initializes the database (if not already created) to be used throughout this project.
    filename.db will be found in the current working directory. 
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def create_spotifyartists_table(favartists, token, offset, cur, conn):
    '''
    This function takes in a list of artists, a token, an offset, and a database cur/conn.
    It then creates a table inside the database pointed to by cur/conn with an artist's information
    which includes artist id, name, spotiy followers, and number of tracks available on spotify.
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS spotifyartists (artistid INTEGER PRIMARY KEY UNIQUE, artistname TEXT, numfollowers INTEGER, numtracks INTEGER)")
    for i in range(len(list(favartists.values()))):
        insertval = spot_data_one(list(favartists.values())[i], token, offset)
        cur.execute("INSERT OR IGNORE INTO spotifyartists (artistid,artistname,numfollowers,numtracks) VALUES (?,?,?,?)",(i, insertval[0], insertval[1], insertval[2])) 
    conn.commit()

def create_spotifyalbums_table(favartists, token, offset, cur, conn):
    '''
    This function takes in a list of artists, a token, an offset, and a database cur/conn.
    It then creates a table inside the database pointed to by cur/conn with each artist's discography information
    which includes artist id, album name, spotify, length of project, and release date.
    '''
    cur.execute("CREATE TABLE IF NOT EXISTS spotifyalbums (artistid INTEGER, albumname TEXT UNIQUE PRIMARY KEY, length INTEGER, releasedate STRING)")
    for i in range(len(list(favartists.values()))):
        insertval = spot_data_two(list(favartists.values())[i], token, offset)
        for album in insertval:
            cur.execute("INSERT OR IGNORE INTO spotifyalbums (artistid,albumname,length,releasedate) VALUES (?,?,?,?)", (i, album[0], album[1], album[2]))
    conn.commit()

def artistalbumsurl(artistid):
    '''
    Given an artist ID, this function returns an API url to access all of their albums.
    '''
    return "https://api.spotify.com/v1/artists/" + artistid + "/albums"

def albumurl(albumid):
    '''
    Given an album id, this function returns an API url to access a specific album.
    '''
    return "https://api.spotify.com/v1/albums/" + albumid

def artisturl(artistid):
    '''
    Given an album id, this function returns an API url to access a specific artist.
    '''
    return "https://api.spotify.com/v1/artists/" + artistid

def spot_data_two(artistid, token, offset): 
    '''
    This function takes in an artist id and generates a list of tuples which will be 
    used to populate the albums table with entries about each of the artist's releases.
    '''
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

def spot_data_one(artistid, token, offset): 
    '''
    This function takes in an artist id and generates tuple about the artist's 
    name, number of spotify followers, and total tracks available on spotify.
    '''
    url = artisturl(artistid)
    param = {'limit': 25,'offset': offset, 'access_token': token}
    response = requests.get(url, params = param)
    results = response.json()
    artistname = results['name']
    numfollowers = int(results['followers']['total'])
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
    return (artistname, numfollowers, totaltracks)

def main():
    favartists = {'Ed sheeran' : '6eUKZXaKkcviH0Ku9w2n3V',
    'The Weeknd' : '1Xyo4u8uXC1ZmMpatF05PJ',  
    'Billie Eilish'	: '6qqNVTkY8uBg9cP3Jd7DAH',
    'Justin Bieber' : '1uNFoZAHBGtllmzznpCI3s',
    'Taylor Swift' : '06HL4z0CvFAxyc27GXpf02',
    'Drake' : '3TVXtAsR1Inumwj472S9r4',
    'Eminem' : '7dGJo4pcD2V6oG8kP0tJRR',
    'Post Malone' : '246dkjvS1zLTtiykXe5h60',
    'Kanye West' : '5K4W6rqBFWDnAN6FQUkS6x',
    'Juice Wrld' :'4MCBfE4596Uoi2O4DtmEMz'}
    
    #must update token every time :/ go to https://developer.spotify.com/console/get-album/  
    token = 'BQAYu3ZDagSKs6xQryTBPtTKQH1lMRrnw3KtlXG9HZRhGPSpHs99vltqxvC9GhDi9WXxJl8_5b7YyLYp9LRGtLBxOxI_ySPnbWEUHFhmTe_qy7oDqYqow6IcQabF9qrpSjRRg4dsNooScJ3tEZf9A3kIqoI62KdNgeQ'
    start = 0
    cur, conn = createDB('twittertest.db')
    create_spotifyartists_table(favartists, token, start, cur, conn)
    create_spotifyalbums_table(favartists, token, start, cur, conn)

main()