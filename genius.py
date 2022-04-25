import requests, json

# constants
BASE_URL = "https://api.genius.com"
TOKEN = "GXbwC9RH0ntDv_KvahB_M7iVeqxQN4d0oruo68Da2kE2wFtj-kX96U5Rux_b9rvs"
# ARTIST_NAMES = ['Ed Sheeran', 'The Weeknd', 'Ariana Grande', 'Justin Bieber', 'Taylor Swift', 'Drake', 'Eminem', 'Post Malone', 'Kanye West', 'Juice Wrld']
ARTIST_NAMES = ['Ed Sheeran']

# send request and get response in json format
def start(path, params = None, headers = None):

    # generate request URL
    url = BASE_URL + "/" + path
    token = "Bearer " + TOKEN
    if headers:
        headers['Authorization'] = token
    else:
        headers = {"Authorization": token}

    response = requests.get(url = url, params = params, headers = headers)
    response.raise_for_status()

    return response.json()

def get_artist_followers(artist_id):
    path = "artists/" + str(artist_id)
    data = start(path = path)

    followers = data["response"]["artist"]["followers_count"]
    return followers

def get_artist_songs(artist_id):
    current_page = 1
    next_page = True 
    songs = []

    while next_page:

        path = "artists/" + str(artist_id) + "/songs/"
        params = {'page': current_page}
        data = start(path = path, params = params)

        page_songs = data['response']['songs']
        # print(data['response'])

        if page_songs:
            # add all the songs of current page,
            # and increment current_page value for next loop
            songs += page_songs
            current_page += 1
        else:
            # if page_songs is empty, quit
            next_page = False

    # get all the song ids, excluding not-primary-artist songs
    songs = [song["id"] for song in songs if song["primary_artist"]["id"] == artist_id]

    return songs

def get_song_names(song_ids):
    song_lst = {}

    for i, song_id in enumerate(song_ids):
        path = "songs/" + str(song_id)
        
        data = start(path = path)["response"]["song"]

        if data["primary_artist"]["name"] not in song_lst.keys():
            song_lst[data["primary_artist"]["name"]] = [data["title"]]
        else:
            song_lst[data["primary_artist"]["name"]] += [data["title"]]

    print(song_lst)
    return song_lst

# just added, may not work
def get_song_date(song_ids):
    song_lst2 = {}

    for i, song_id in enumerate(song_ids):
        path = "songs/" + str(song_id)
        
        data = start(path = path)["response"]["song"]

        if data["release_date"] not in song_lst2.keys():
            song_lst2["release_date"] = data["release_date"]
        else:
            song_lst2["release_date"] = data["release_date"]

    print(song_lst2)
    return song_lst2


# # # 

# artist
for artist in ARTIST_NAMES:
    print("searching " + artist + "'s artist id. \n")

    find_id = start("search", {'q': artist})
    for a in find_id["response"]["hits"]:
        if a["result"]["primary_artist"]["name"] == artist:
            artist_id = a["result"]["primary_artist"]["id"]
            break
    # get all song ids and make a list
    song_ids = get_artist_songs(artist_id)
    # finally, make a full list of songs names
    full_list_of_songs = get_song_names(song_ids)
    #get the artist's genius follower count
    print(get_artist_followers(artist_id))

# for artist in ARTIST_NAMES:
#     find_id = start("search", {'q': artist})
#     for b in find_id["response"]["hits"]:
#         if b["result"]["primary_artist"]["name"] == artist:
#             artist_id = b["result"]["primary_artist"]["id"]
#             break
