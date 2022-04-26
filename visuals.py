import sqlite3
import json
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegFileWriter
import numpy as np
import csv

def graph_avg_followers(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT artistname FROM spotifyartists")    
    namelist = [x[0] for x in cur.fetchall()]
    averages = []
    cur.execute("SELECT soundcloud_artists.num_followers, twitter.follower_count, spotifyartists.numfollowers FROM twitter INNER JOIN soundcloud_artists ON twitter.artist_id = soundcloud_artists.artist_id INNER JOIN spotifyartists ON twitter.artist_id = spotifyartists.artistid")
    for item in cur.fetchall():
        averages.append(sum(item)//3)
    
    write_to_csv('avg_followers.csv', ['artist name', 'number of followers'], [namelist, averages])

    plt.figure(dpi = 65)
    plt.bar(namelist, averages)
    plt.xlabel('Artist Name')
    plt.ylabel('Number of Followers (in Tens of Millions)')
    plt.title('Average Followers per Artist Across Platforms')
    plt.show()

def graph_num_tracks(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT artistname FROM spotifyartists")    
    namelist = [x[0] for x in cur.fetchall()]
    sccounts = []
    spotcounts = []
    cur.execute("SELECT soundcloud_artists.num_tracks, spotifyartists.numtracks FROM soundcloud_artists JOIN spotifyartists ON spotifyartists.artistid = soundcloud_artists.artist_id")
    for item in cur.fetchall():
        sccounts.append(item[0])
        spotcounts.append(item[1])
    
    write_to_csv('num_tracks_available.csv', ['artist name', 'soundcloud tracks', 'spotify tracks'], [namelist, sccounts, spotcounts])

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
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT artistname FROM spotifyartists")    
    namelist = [x[0] for x in cur.fetchall()]
    cur.execute("SELECT AVG(length) FROM spotifyalbums GROUP BY artistid")
    averages = [float(x[0]) for x in cur.fetchall()]

    write_to_csv('avg_album_length.csv', ['artist name', 'number of tracks'], [namelist, averages])

    plt.figure(dpi = 65)
    plt.bar(namelist, averages)
    plt.xlabel('Artist Name')
    plt.ylabel('Average Album Length')
    plt.title('Average Number of Tracks on Albums')
    plt.show()

def write_to_csv(filename, headerlist, datalists):
    with open(filename, 'w', newline='') as f:
        cwriter = csv.writer(f)
        headline = [x for x in headerlist]
        cwriter.writerow(headline) 
        for i in range(len(datalists[0])):
            temp = []
            for j in datalists:
                temp.append(j[i])
            cwriter.writerow(temp)

def main():
    ans = int(input("enter a number to generate a graph:\n1 for avg followers across platforms\n2 for number of tracks available on platforms\n3 for average album length\n"))
    if ans == 1:
        graph_avg_followers('finalproj.db')
    if ans == 2:
        graph_num_tracks('finalproj.db')
    if ans == 3:
        graph_avg_album_length('finalproj.db')

main()