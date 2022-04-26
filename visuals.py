import sqlite3
import json
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegFileWriter
import numpy as np

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
    
    x_axis = np.arange(len(namelist))  
    plt.bar(x_axis - 0.2, sccounts, 0.4, label = 'SoundCloud')
    plt.bar(x_axis + 0.2, spotcounts, 0.4, label = 'Spotify')
    plt.xticks(x_axis, namelist)
    plt.xlabel("Artist")
    plt.ylabel("Number of Tracks")
    plt.title("Number of Tracks Available on Platform")
    plt.legend()
    plt.show()

def main():
    #graph_avg_followers('finalproj.db')
    graph_num_tracks('finalproj.db')

main()