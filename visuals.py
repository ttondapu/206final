import sqlite3
import json
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegFileWriter
import numpy as np
import csv

def graph_avg_followers(db_filename):
    '''
    Given the database, this function outputs a csv file to the current directory and 
    displays a bar chart visualizing each artist's average follower count across 
    twitter, spotify, and soundcloud.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT artistname FROM spotifyartists")    
    namelist = [x[0] for x in cur.fetchall()]
    averages = []
    cur.execute("SELECT soundcloud_artists.num_followers, twitter.follower_count, spotifyartists.numfollowers FROM twitter INNER JOIN soundcloud_artists ON twitter.artist_id = soundcloud_artists.artist_id INNER JOIN spotifyartists ON twitter.artist_id = spotifyartists.artistid")
    for item in cur.fetchall():
        averages.append(sum(item)//3)
    
    write_to_csv('avg_followers.csv', ['artist name', 'average number of followers across platforms'], [namelist, averages])

    plt.figure(dpi = 65)
    plt.bar(namelist, averages)
    plt.xlabel('Artist Name')
    plt.ylabel('Number of Followers (in Tens of Millions)')
    plt.title('Average Followers per Artist Across Platforms')
    plt.show()

def graph_num_tracks(db_filename):
    '''
    Given the database, this function outputs a csv file to the current directory and 
    displays a bar chart visualizing the number of tracks available on soundcloud
    and spotify respectively for each artist.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT artistname FROM spotifyartists")    
    namelist = [x[0] for x in cur.fetchall()]
    cur.execute("SELECT  numtracks FROM spotifyartists")
    spotcounts = [x[0] for x in cur.fetchall()]
    cur.execute("SELECT COUNT(track_name) FROM soundcloud_tracks GROUP BY artist_id")
    sccounts = [x[0] for x in cur.fetchall()]
    
    write_to_csv('num_tracks_available.csv', ['artist name', 'number of soundcloud tracks', 'number of spotify tracks'], [namelist, sccounts, spotcounts])

    x_axis = np.arange(len(namelist))  
    plt.bar(x_axis - 0.2, sccounts, 0.4, label = 'SoundCloud')
    plt.bar(x_axis + 0.2, spotcounts, 0.4, label = 'Spotify')
    plt.xticks(x_axis, namelist)
    plt.xlabel("Artist")
    plt.ylabel("Number of Tracks")
    plt.title("Number of Tracks Available on Platform")
    plt.legend()
    plt.show()

def graph_avg_album_length(db_filename):
    '''
    Given the database, this function outputs a csv file to the current directory and 
    displays a bar chart of each artist's average album length based on all of their releases.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT artistname FROM spotifyartists")    
    namelist = [x[0] for x in cur.fetchall()]
    cur.execute("SELECT AVG(length) FROM spotifyalbums GROUP BY artistid")
    averages = [float(x[0]) for x in cur.fetchall()]

    write_to_csv('avg_album_length.csv', ['artist name', 'average number of tracks per album'], [namelist, averages])

    plt.figure(dpi = 65)
    plt.bar(namelist, averages)
    plt.xlabel('Artist Name')
    plt.ylabel('Average Album Length')
    plt.title('Average Number of Tracks on Albums')
    plt.show()

def write_to_csv(filename, headerlist, datalists):
    '''
    Given a desired output file name, a list of headers, and a list of data lists,
    this function writes a csv file where each entry contains a values from the lists.
    This is used as a helper function inside the visualization/generation functions.
    '''
    with open(filename, 'w', newline='') as f:
        cwriter = csv.writer(f)
        headline = [x for x in headerlist]
        cwriter.writerow(headline) 
        for i in range(len(datalists[0])):
            temp = []
            for j in datalists:
                temp.append(j[i])
            cwriter.writerow(temp)

def main(db_filename):
    '''
    Main will prompt for a number representing the three visualization options.
    It will create/connect to the database passed in to access the five tables.
    Upon entering a number, a csv file will be created and a graphic will pop up.
    '''
    ans = int(input("enter a number to generate a graph:\n1 for avg followers across platforms\n2 for number of tracks available on platforms\n3 for average album length\n"))
    if ans == 1:
        graph_avg_followers(db_filename)
    if ans == 2:
        graph_num_tracks(db_filename)
    if ans == 3:
        graph_avg_album_length(db_filename)

main('finalproj.db')