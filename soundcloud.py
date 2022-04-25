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

# def get_url(artist_user):
#     url = 'https://soundcloud.com/'+ artist_user + '/albums'
#     return url

def artist_followers(artist_html):

    '''
    generates the number of followers for a given artist and file saved from an artist's SoundCloud page

    '''
    with open(artist_html) as f:
        soup = bs(f, 'html.parser')
    # page = requests.get(url)
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
    print(num_tracks)  
    return num_tracks



#line 1694
artists = { #change
    'Ed Sheeran': ['edsheeran'], 
    'Olivia Rodrigo': ['oliviarodrigo', 'olivia_rodrigo.html'], 
    'The Weeknd': ['theweeknd'],
    'Ariana Grande': ['arianagrande'],
    'Taylor Swift': ['taylorswiftofficial'],
    'Drake': ['octobersveryown'],
    'Eminem': ['eminemofficial'],
    'Post Malone': ['postmalone'],
    'Kanye West': ['kanyewest'],
    'Juice Wrld': ['uiceheidd']
}


track_count('olivia_rodrigo.html')