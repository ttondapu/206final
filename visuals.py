import sqlite3
import json
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegFileWriter

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






def main():
    #graph_avg_followers('finalproj.db')

main()