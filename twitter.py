import requests
import os
import json

bearer_token = 'AAAAAAAAAAAAAAAAAAAAAIRqbwEAAAAAsGxXkoOd1FhqAr6cwMKspjB0ioM%3DUwmyqZIUbs3R5VLdmN8XUe0y5S1eLzlAnRGW33CWMAafORu9Ik'

def create_url(user_id):
    '''
    returns an api url given an artist's twitter id
    '''
    return "https://api.twitter.com/2/users/{}?user.fields=public_metrics".format(user_id)

def bearer_oauth(r):
    """
    from twitter site to authorize
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FollowerLookupPython"
    return r

def get_artist_info(url):
    response = requests.request("GET", url, auth=bearer_oauth, params={})
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))
    json_response = response.json()
    return((json_response['data']['username'], json_response['data']['public_metrics']['followers_count'], json_response['data']['public_metrics']['tweet_count']))

def main():
    url = create_url(1599608046) 
    #lil uzi vert for example
    print(get_artist_info(url))

main()