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

def get_html(artist_user):
    url = 'https://soundcloud.com/'+ artist_user + '/albums'
    page = requests.get(url)
    return page.text

def artist_followers(artist_html):

    '''
    generates the number of followers for a given artist and file saved from an artist's SoundCloud page

    '''
    # with open(artist_html) as f:
    #     soup = bs(f, 'html.parser')
    soup = bs(artist_html, 'html.parser')
    soup.prettify()   
    num_followers = soup.find('a', class_ = "infoStats__statLink sc-link-light sc-link-primary").get('title')
    s = num_followers.split()
    s = s[0].replace(',', '') #to get rid of commas
    num = int(s) #to make integer
    return num

def album_count(artist_html):
    num_albums = 0
    # with open(artist_html) as f:
    #     soup = bs(f, 'html.parser')
    soup = bs(artist_html, 'html.parser')
    soup.prettify()
    album_list = []
    album_tag = soup.find_all('a', class_ = "sc-link-primary soundTitle__title sc-link-dark sc-text-h4")
    for tag in album_tag:
        title = tag.find('span', class_="").text.strip()
        album_list.append(title)
    for album in album_list:
        num_albums += 1
    return num_albums


#line 1694
artists = {
    'Ed Sheeran': ['edsheeran'], 
    'Olivia Rodrigo': ['oliviarodrigo'], 
    'The Weeknd': ['theweeknd'],
    'Ariana Grande': ['arianagrande'],
    'Taylor Swift': ['taylorswiftofficial'],
    'Drake': ['octobersveryown'],
    'Eminem': ['eminemofficial'],
    'Post Malone': ['postmalone'],
    'Kanye West': ['kanyewest'],
    'Juice Wrld': ['uiceheidd']
}

pretty(get_html(artists['Olivia Rodrigo'][0]))

# def main():
#     print('hi')
