import requests, json

# constant vals
BASE_URL = "https://api.genius.com"
TOKEN = "GXbwC9RH0ntDv_KvahB_M7iVeqxQN4d0oruo68Da2kE2wFtj-kX96U5Rux_b9rvs"
ARTIST_NAMES = ['Ed Sheeran', 'The Weeknd', 'Ariana Grande', 'Justin Bieber', 'Taylor Swift', 'Drake', 'Eminem', 'Post Malone', 'Kanye West', 'Juice Wrld']

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

def get_artist_songs(artist_id):
    # initialize variables & a list
    current_page = 1
    next_page = True 
    songs = []

    # main loop
    while next_page:

        path = "artists/" + str(artist_id) + "/songs/"
        params = {'page': current_page}
        data = start(path = path, params = params)

        page_songs = data['response']['songs']

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
    # initialize a dictionary
    song_lst = {}

    i = 0

    # main loop
    for i, song_id in enumerate(song_ids):
        print("id:" + str(song_id) + " start. ->")

        path = "songs/" + str(song_id)
        data = start(path = path)["response"]["song"]

        song_lst[data["primary_artist"]["name"]] = []

        song_lst[data["primary_artist"]["name"]] += [data["title"]]


        # song_lst[i] = {
        #     "artist": data["primary_artist"]["name"],
        #     "title": data["title"],
        #     "album": data["album"]["name"] if data["album"] else "<single>",
        #     "release_date": data["release_date"] if data["release_date"] else "unidentified",
        #     "featured_artists":
        #         [feat["name"] if data["featured_artists"] else "" for feat in data["featured_artists"]],
        #     "producer_artists":
        #         [feat["name"] if data["producer_artists"] else "" for feat in data["producer_artists"]],
        #     "writer_artists":
        #         [feat["name"] if data["writer_artists"] else "" for feat in data["writer_artists"]],
        #     "genius_track_id": song_id
        #     "genius_album_id": data["album"]["id"] if data["album"] else "none"}

        print("-> id:" + str(song_id) + " is finished. \n")

    print(song_lst)
    return song_lst

# # # 

for artist in ARTIST_NAMES:
    print("searching " + artist + "'s artist id. \n")

    # find artist id from given data
    find_id = start("search", {'q': artist})
    for a in find_id["response"]["hits"]:
        if a["result"]["primary_artist"]["name"] == artist:
            artist_id = a["result"]["primary_artist"]["id"]
            break

    print("-> " + artist + "'s id is " + str(artist_id) + "\n")

    print("getting song ids. \n")

for artist in ARTIST_NAMES:

    # find artist id from given data
    find_id = start("search", {'q': artist})
    for b in find_id["response"]["hits"]:
        if b["result"]["primary_artist"]["name"] == artist:
            artist_id = b["result"]["primary_artist"]["id"]
            break

    # get all song ids and make a list
    song_ids = get_artist_songs(artist_id)

    print("\n-> got all the song ids. take a break for a while \n")

    print("getting meta data of each song. \n")

    # finally, make a full list of songs with meta data
    full_list_of_songs = get_song_names(song_ids)

    print("-> Mission complete! Check it out!")