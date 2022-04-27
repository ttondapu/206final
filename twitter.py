import requests
from bs4 import BeautifulSoup as bs
import json
import os
import matplotlib
import sqlite3
import matplotlib.pyplot as plt

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIRqbwEAAAAA2q5wMs3ND0cdnL%2FvWx%2FdoHP9szw%3Do1nyawbrzdzaYDeMM5dmulc0jwhvRHg9WWm68Rb6HAa6QafGmI'

def createDB(filename):
    '''
    This function initializes the database (if not already created) to be used throughout this project.
    filename.db will be found in the current working directory. 
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def setUpTwitterTable(favartists, keyrange, counter, cur, conn):
    '''
    This function takes in a list of artists and a cur/conn pointing to a database. 
    When run, it will populate the twitter table inside the database, inserting an entry for each 
    artist including information about their username, number of followers, and number of tweets.
    '''
    cur.execute('CREATE TABLE IF NOT EXISTS twitter (artist_id INTEGER UNIQUE PRIMARY KEY, twitter_handle TEXT, follower_count INTEGER, tweet_count INETEGER)')
    for i in keyrange:
        print(i)
        url = create_url(favartists[i])
        data = get_artist_info(url)
        twitter_handle = data[0]
        follower_count = data[1]
        tweet_count = data[2]
        artist_id = counter
        cur.execute("INSERT OR IGNORE INTO twitter (artist_id, twitter_handle, follower_count, tweet_count) VALUES (?,?,?,?)", (artist_id, twitter_handle, follower_count, tweet_count))
        counter += 1
    conn.commit()

def create_url(user_id):
    '''
    This function takes in a twitter user id and returns a url to access their account from the API.
    '''
    return "https://api.twitter.com/2/users/{}?user.fields=public_metrics".format(user_id)

def bearer_oauth(r):
    '''
    DO NOT EDIT: This function is from the twitter dev site to authorize our program.
    It utilizes the bearer token found at the top.
    '''
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowerLookupPython"
    return r

def get_artist_info(url):
    '''
    This function takes a twitter api url and returns the json response object.
    '''
    response = requests.request("GET", url, auth=bearer_oauth, params={})
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
    json_response = response.json()
    return((json_response['data']['username'], json_response['data']['public_metrics']['followers_count'], json_response['data']['public_metrics']['tweet_count']))

def main(dbfilename):
    '''
    main() prompts the user for a number 1-4 and will populate the twitter table in the database passed in.
    to fully populate, run 4 times and each time type in 1/2/3/4 in that order to fill all 100 entries.
    '''
    favartists = {'Ed Sheeran' : '85452649',
    'The Weeknd' : '255388236',  
    'Billie Eilish'	: '2150327072',
    'Justin Bieber' : '27260086',
    'Taylor Swift' : '17919972',
    'Drake' : '27195114',
    'Eminem' : '22940219',
    'Post Malone' : '913812620',
    'Kanye West' : '169686021',
    'Juice Wrld' :'3676932858',
    'Bad Bunny': '1059542139737128960',
    'BTS': '335141638',
    'J Balvin':'44670915',
    'Coldplay':'18863815',
    'XXXTENTACION':'754101056',
    'Ozuna':'4873308778',
    'Dua Lipa':'154101116',
    'Khalid':'1852644804',
    'Imagine Dragons':'75916180',
    'Travis Scott':'135019364',
    'Rihanna':'79293791',
    'Maroon 5':'24886570',
    'Shawn Mendes':'379408088',
    'David Guetta':'23976386',
    'Bruno Mars':'100220864',
    'Calvin Harris':'18625669',
    'Daddy Yankee':'36483808',
    'Sam Smith':'457554412',
    'Queen':'98765275',
    'Kendrick Lamar':'23561980',
    'The Chainsmokers':'36746176',
    'One Direction':'209708391',
    'Chris Brown':'119509520',
    'Beyoncé':'31239408',
    'Future':'51742969',
    'Anuel AA':'703558015862104064',
    'Nicki Minaj':'35787166',
    'Lady Gaga':'14230524',
    'J. Cole':'19028953',
    'Halsey':'45709328',
    'Selena Gomez':'23375688',
    'Adele':'184910040',
    'The Beatles':'27760317',
    'Sia':'23497233',
    'Maluma':'153433497',
    'Twenty One Pilots':'59325073',
    'Marshmello':'2987922767',
    'Lil Uzi Vert':'34485937',
    'Linkin Park':'19373710',
    'Kygo':'1951639321',
    'Katy Perry':'21447363',
    'Avicii':'27476141',
    'Farruko':'69413371',
    'Little Mix':'380399508',
    'Camila Cabello':'739784130',
    'Rauw Alejandro':'1330718940',
    'Jason Derulo':'28076276',
    'Red Hot Chili Peppers':'297047872',
    'Demi Lovato':'21111883',
    'Arctic Monkeys':'49636886',
    'Doja Cat':'568545739',
    'Shakira':'44409004',
    'Harry Styles':'181561712',
    'KAROL G':'78335735',
    'Nicky Jam':'246967511',
    'OneRepublic':'21133007',
    'Miley Cyrus':'268414482',
    'Michael Jackson':'54387680',
    'Martin Garrix':'134234000',
    'Charlie Puth':'15945351',
    'Pitbull':'31927467',
    'Sebastian Yatra':'1029323618',
    'G-Eazy':'17936793',
    'Panic! At The Disco':'16213013',
    'DaBaby':'3004871415',
    'Cardi B':'866953267',
    'Major Lazer':'30513101',
    'Lil Baby':'816412233488015360',
    'Ellie Goulding':'20565284',
    'Lil Wayne':'116362700',
    'Young Thug':'238763290',
    '21 Savage':'260114837',
    'Pop Smoke':'1131025001434497024',
    'Wiz Khalifa':'20322929',
    'Sech':'837110334800424960',
    'Mac Miller':'23065354',
    'Myke Towers':'302856349',
    'Diplo':'17174309',
    'Metallica':'238475531',
    'Fall Out Boy':'16212952',
    'Lil Nas X':'754006735468261376',
    'Lil Peep':'2586341939',
    'Logic':'141944292',
    'Alan Walker':'2561704644',
    'Migos':'353029369',
    'Tyga':'22733444',
    'John Mayer':'335534204',
    'P!nk':'28706024',
    'AC/DC':'2836755090',
    'ZAYN':'176566242'} 
    cur, conn = createDB(dbfilename)
    ans = int(input("enter a number 1-4 (representing a quarter of entries to insert): "))
    if ans == 1:
        setUpTwitterTable(favartists, list(favartists.keys())[0:25], 0, cur, conn)
    elif ans == 2:
        setUpTwitterTable(favartists, list(favartists.keys())[25:50], 25, cur, conn)
    elif ans == 3:
        setUpTwitterTable(favartists, list(favartists.keys())[50:75], 50, cur, conn)
    elif ans == 4:
        setUpTwitterTable(favartists, list(favartists.keys())[75:100], 75, cur, conn)

main('finalproj.db')