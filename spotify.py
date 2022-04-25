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

def create_spotifyartists_table(favartists, token, offset, cur, conn):
    cur.execute("DROP TABLE IF EXISTS spotifyartists")
    cur.execute("CREATE TABLE IF NOT EXISTS spotifyartists (artistid INTEGER PRIMARY KEY UNIQUE, artistname TEXT, numfollowers INTEGER, numtracks INTEGER)")
    for i in range(len(list(favartists.values()))):
        insertval = spot_data_one(list(favartists.values())[i], token, offset)
        cur.execute("INSERT OR IGNORE INTO spotifyartists (artistid,artistname,numfollowers,numtracks) VALUES (?,?,?,?)",(i, insertval[0], insertval[1], insertval[2])) 
    conn.commit()

def create_spotifyalbums_table(favartists, token, offset, cur, conn):
    counter = 0
    cur.execute("DROP TABLE IF EXISTS spotifyalbums")
    cur.execute("CREATE TABLE IF NOT EXISTS spotifyalbums (artistid INTEGER, albumid TEXT, albumname TEXT UNIQUE PRIMARY KEY, length INTEGER, releasedate STRING)")
    for i in range(len(list(favartists.values()))):
        insertval = spot_data_two(list(favartists.values())[i], token, offset)
        for album in insertval:
            cur.execute("INSERT OR IGNORE INTO spotifyalbums (artistid,albumid,albumname,length,releasedate) VALUES (?,?,?,?,?)", (i, counter, album[0], album[1], album[2]))
            counter += 1 #increment unique id, but this skips sometimes because artists have duplicates
    conn.commit()

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

def spot_data_two(artistid, token, offset): 
    '''
    returns list of an artist's releases with number of tracks and release date
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
    returns tuple of an artist's info including name, total number of tracks on albums, and number of followers
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
    'Ariana Grande'	: '66CXWjxzNUsdJxJ2JdwvnR',
    'Justin Bieber' : '1uNFoZAHBGtllmzznpCI3s',
    'Taylor Swift' : '06HL4z0CvFAxyc27GXpf02',
    'Drake' : '3TVXtAsR1Inumwj472S9r4',
    'Eminem' : '7dGJo4pcD2V6oG8kP0tJRR',
    'Post Malone' : '246dkjvS1zLTtiykXe5h60',
    'Kanye West' : '5K4W6rqBFWDnAN6FQUkS6x',
    'Juice Wrld' :'4MCBfE4596Uoi2O4DtmEMz'}
    
    '''
    try:
        cur.execute('SELECT name FROM spotify_results WHERE name  = ')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0
    '''

    start = 0
    #must update token every time :/ go to https://developer.spotify.com/console/get-album/
    token = 'BQCwrYVcmzc1HggMwAtdobeyFLu9dfxxSFkfC3yZeTFaKIeRQcCv6wIsN9j3wc461aU7HqTCSbYx4i8U-x6TQtW7uXiLQBYYZatTfo-SH1B_UdA-cts9mmITjpGnO_rladXG_sPdmAXyWb3caIJ_iNwfZLFOodojBE8'
    cur, conn = createDB('spotify.db')
    create_spotifyartists_table(favartists, token, start, cur, conn)
    create_spotifyalbums_table(favartists, token, start, cur, conn)

main()