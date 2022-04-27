import requests
from bs4 import BeautifulSoup as bs
import json
import os
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

def setUpSoundcloudArtistTable(favartists, cur, conn):
    '''
    This function takes in a list of artists, a token, an offset, and a database cur/conn.
    It then creates a table inside the database pointed to by cur/conn with an artist's information
    which includes artist id, name, soundcloud followers (and formerly number of tracks available on soundcloud).
    '''
    cur.execute('CREATE TABLE IF NOT EXISTS soundcloud_artists (artist_id INTEGER UNIQUE PRIMARY KEY, name TEXT, num_followers INETEGER)')
    counter = 0
    for i in favartists.keys():
        artist_id = counter
        name = i
        num_followers = artist_followers(favartists[i])
        cur.execute("INSERT OR IGNORE INTO soundcloud_artists (artist_id, name, num_followers) VALUES (?,?,?)", (artist_id, name, num_followers))
        counter+=1
    conn.commit()

def setUpSoundcloudTrackTable(favartists, cur, conn):
    '''
    This function takes in a list of artists, a token, an offset, and a database cur/conn.
    It then creates a table inside the database pointed to by cur/conn with each track for each artist,
    in the form of artist id, track name.
    '''
    cur.execute('CREATE TABLE IF NOT EXISTS soundcloud_tracks (artist_id INTEGER, track_name TEXT PRIMARY KEY UNIQUE)')
    counter = 0
    for i in favartists.keys(): 
        print(i)   
        artist_id = counter
        counter += 1
        tracks = all_tracks(favartists[i])
        for track in tracks:
            cur.execute("INSERT OR IGNORE INTO soundcloud_tracks (artist_id, track_name) VALUES (?,?)", (artist_id, track))
    conn.commit()

def get_url(artist_user):
    '''
    This function generates a url to access the html of an artist's tracks 
    '''
    return 'https://soundcloud.com/'+ artist_user + '/tracks'

def artist_followers(artist_html):
    '''
    This function returns the number of followers for a given artist from an artist's SoundCloud page html.
    '''
    with open(artist_html) as f:
        soup = bs(f, 'html.parser')
    num_followers = soup.find('a', class_ = "infoStats__statLink sc-link-light sc-link-primary").get('title')
    s = num_followers.split()
    s = s[0].replace(',', '') #to get rid of commas
    num = int(s) #to make integer
    return num

def all_tracks(artist_html):
    '''
    This function takes an artist's soundcloud html and returns a list of track titles for all tracks available
    '''
    with open(artist_html) as f:
        soup = bs(f, 'html.parser')
    track_list = []
    track_tag = soup.find_all('a', class_ = "sc-link-primary soundTitle__title sc-link-dark sc-text-h4")
    for tag in track_tag:
        title = tag.find('span').text
        track_list.append(title)
    return track_list

def main(db_filename):
    favartists = {'Ed Sheeran' : 'ed_sheeran.html',
    'The Weeknd' : 'the_weeknd.html',  
    'Billie Eilish'	: 'billie_eilish.html',
    'Justin Bieber' : 'justin_bieber.html',
    'Taylor Swift' : 'taylor_swift.html', 
    'Drake' : 'drake.html', 
    'Eminem' : 'eminem.html', 
    'Post Malone' : 'post_malone.html', 
    'Kanye West' : 'kanye_west.html',
    'Juice Wrld' :'juice_wrld.html'}

    cur, conn = createDB(db_filename)
    setUpSoundcloudArtistTable(favartists, cur, conn)
    setUpSoundcloudTrackTable(favartists, cur, conn)

main('finalproj.db')