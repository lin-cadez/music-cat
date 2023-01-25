from youtubesearchpython import VideosSearch
import json
import spotipy
import webbrowser
import requests
def get_song_data(iskanje):
    try:

        videosSearch = VideosSearch(iskanje, limit=1)
        song_search = videosSearch.result()["result"][0]["title"]
        with open('creds.json') as f:
            creds = json.load(f)
        CLIENT_ID = creds["CLIENT_ID"]
        CLIENT_SECRET = creds["CLIENT_SECRET"]
        AUTH_URL = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(AUTH_URL, {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })

        auth_response_data = auth_response.json()
        access_token = auth_response_data['access_token']
        headers = {
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
        BASE_URL = 'https://api.spotify.com/v1/'
        r = requests.get(BASE_URL + 'search?q=' + song_search +
                        '&type=track&market=US&limit=1&offset=0', headers=headers)
        r = r.json()
        re = r['tracks']['items'][0]
        release_date = r['tracks']['items'][0]['album']['release_date'][:4:]
        artist = r['tracks']['items'][0]['artists'][0]['name']
        title=re['name']


        return title, artist, release_date
    except:
        return "","",""



