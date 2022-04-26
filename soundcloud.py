import requests
from bs4 import BeautifulSoup as bs
import json
import os
import matplotlib
import sqlite3
import matplotlib.pyplot as plt
from sqlalchemy import all_

#user_agent = {'User-agent': 'Mozilla/5.0'}

def createDB(filename):
    '''
    initializes database
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def setUpSoundcloudArtistTable(favartists, cur, conn):
    cur.execute('DROP TABLE IF EXISTS soundcloud_artists')
    cur.execute('CREATE TABLE soundcloud_artists (artist_id INTEGER UNIQUE PRIMARY KEY, name TEXT, num_tracks INTEGER, num_followers INETEGER)')
    counter = 0
    for i in favartists.keys():
        artist_id = counter
        name = i
        num_tracks = track_count(favartists[i])
        num_followers = artist_followers(favartists[i])
        cur.execute("INSERT OR IGNORE INTO soundcloud_artists (artist_id, name, num_tracks, num_followers) VALUES (?,?,?,?)", (artist_id, name, num_tracks, num_followers))
        counter+=1
    conn.commit()

def setUpSoundcloudTrackTable(favartists, cur, conn): #TODO
    cur.execute('DROP TABLE IF EXISTS soundcloud_tracks')
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
     url = 'https://soundcloud.com/'+ artist_user + '/tracks'
     return url

def artist_followers(artist_html):

    '''
    generates the number of followers for a given artist and file saved from an artist's SoundCloud page

    '''
    with open(artist_html) as f:
        soup = bs(f, 'html.parser')
    # page = requests.get(url, headers=user_agent)
    # soup = bs(page.text, 'html.parser')
    num_followers = soup.find('a', class_ = "infoStats__statLink sc-link-light sc-link-primary").get('title')
    s = num_followers.split()
    s = s[0].replace(',', '') #to get rid of commas
    num = int(s) #to make integer
    return num

def track_count(artist_html):
    num_tracks = 0
    with open(artist_html) as f:
        soup = bs(f, 'html.parser')
    # page = requests.get(url)
    # soup = bs(page.text, 'html.parser') #requests
    track_list = []
    track_tag = soup.find_all('a', class_ = "sc-link-primary soundTitle__title sc-link-dark sc-text-h4")
    for tag in track_tag:
        title = tag.find('span', class_ = '')
        track_list.append(title)
    for track in track_list:
        num_tracks += 1 
    return num_tracks

def all_tracks(artist_html):
    with open(artist_html) as f:
        soup = bs(f, 'html.parser')
    # page = requests.get(url)
    # soup = bs(page.text, 'html.parser') #requests
    track_list = []
    track_tag = soup.find_all('a', class_ = "sc-link-primary soundTitle__title sc-link-dark sc-text-h4")
    for tag in track_tag:
        title = tag.find('span').text
        track_list.append(title)
    return track_list


def main():
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

    cur, conn = createDB('finalproj.db')
    #setUpSoundcloudArtistTable(favartists, cur, conn)
    setUpSoundcloudTrackTable(favartists, cur, conn)

main()