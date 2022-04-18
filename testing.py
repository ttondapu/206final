import requests as re
from bs4 import BeautifulSoup as bs
import json
import os

def makeurl(type, id):
    #spotify:artist:4O15NlyKLIASxsJ0PrXPfz
    #spotify:track:4cOdK2wGLETKBW3PvgPWqT
    baseurl = 'https://api.spotify.com/v1/'
    baseurl = baseurl + id + "/" + type
    return baseurl

def getalbum(id, offset): #update token every time
    token = 'BQCpl1GQvjdaI45GItiYDmEgs3ZDVkjxoBQ7Nwsskh7wSXZ-AaMhFyyGQQ7Nt8OkfFCyo8lUqML3hQUoYxPZH4ShWxT8c3iRjk-0RF5KWyoFRNcYCrXN03-mmfhEB9LgNTSRIX5HaTUBX8I'
    url = makeurl("albums", id)
    param = {'limit':25,'offset': offset, 'access_token':token}
    response = re.get(url, params = param)
    data = json.loads(response.text)
    print(data)

def main():
    getalbum("track", "4cOdK2wGLETKBW3PvgPWqT")

main()


