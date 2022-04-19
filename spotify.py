import requests
from bs4 import BeautifulSoup as bs
import json
import os
import sys
import matplotlib
import sqlite3
import unittest
import csv
import matplotlib.pyplot as plt

def createDB(filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+filename)
    cur = conn.cursor()
    return cur, conn

def makeurl(type, id):
    #spotify:artist:4O15NlyKLIASxsJ0PrXPfz
    #spotify:track:4cOdK2wGLETKBW3PvgPWqT
    baseurl = 'https://api.spotify.com/v1/'
    baseurl = baseurl + type + "/" + id
    return baseurl

def getalbum(id, offset): #update token every time :/
    token = 'BQDXWd9VOfS3z_ItPUv4knplzIZpfT_b3y1x7Uy6VSh7FcZ0_vRukhcWlAR9y_O8_sOqRntSHtJBIO-sXz_OdDsI9cK3j0hktveV5qhNHC7nVLzN2xMhDY4dmYV0cZOtipnUUMA-BucOJ4MPIBM9dU09cSIsMLb0znU'
    url = makeurl("albums", id)
    param = {'limit': 25,'offset': offset, 'access_token': token}
    response = requests.get(url, params = param)
    data = json.loads(response.text)
    print(data)

def main():
    cur, conn = createDB('spotify.db')
    getalbum("4O15NlyKLIASxsJ0PrXPfz", "WHAT GOES HERE?")

main()



