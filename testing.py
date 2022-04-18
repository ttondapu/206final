import requests as re
from bs4 import BeautifulSoup as bs
import json
import os

def makeurl(type, id):
    #spotify:artist:4O15NlyKLIASxsJ0PrXPfz?si=vsIQg73TQQ2VmF9FAkTqMQ
    baseurl = 'https://api.spotify.com/'
    baseurl = baseurl + type + ":" + id
    return baseurl

def getdata(type, id):
    url = makeurl(type, id)
    data = json.loads(re.get(url).text)
    print(data)

def main():
    getdata("artist", "4O15NlyKLIASxsJ0PrXPfz")

main()


