import requests
import base64

# TODO

# [x] reload new token on an interval
# [x] pop up window for random playlist
# [x] random playlist to show 10 playlists with 50-100 tracks

# [x] for the longest playlist, we need to implement a for loop to 
#     keep loading in 100 songs; we need to implement an offset value
#     as well, and also every 10 requests we should generate a new token

# [x] doubly linked list for forward / backward playback
# [x] create LL based off original order of playlist
# [ ] to play forward, go from head->next until next is None        # is still array-based, look to change
# [ ] to play backward, go from tail->next until next is None       # is still array-based, look to change

# REFRESH TOKEN #

def get_new_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {}
    data = {}

    # converts client id and client secret to base64, required for security
    message = f"{client_id}:{client_secret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    # set data and headers
    data['grant_type'] = 'client_credentials'
    headers['Authorization'] = f"Basic {base64Message}"

    # send post, extract token from response
    response = requests.post(url=url, headers=headers, data=data)
    token = response.json()['access_token']

    return token

# generate token each time the page is opened to avoid oauth issues 
# my spotify keys (dont steal these please)
client_id = "0b34a65d9de54a1b8b2280ecaa02a6be"
client_secret = "dd9bcf36376648168b60955899678d39"
token = get_new_token(client_id, client_secret)

##### SELECT PLAYLIST FUNCTIONS #####

def get_playlist_tracks(user_id, playlist_id):
    # get the tracks from a specific user's playlist

    response = requests.get(
        f"https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "limit": '10,000',
            "offset": '0'
        }
    )

    return response.json()


def get_users_playlists(user_id):
    # Get the playlists of the user
    # Return array of playlists
    response = requests.get(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    json_response = response.json()


    #return json_response of playlist objects array
    if json_response.get('items'):
        return json_response.get('items')
    return []


def get_tracks_from_playlist(user_id, playlist_name):
    # get tracks of selected playlist

    playlists = get_users_playlists(user_id)
    tracks = [];

    for playlist in playlists:
        if playlist['name'] == playlist_name:
            tracks = get_playlist_tracks(user_id, playlist['id'])

    # return array of tracks for that particular playlist
    if len(tracks) > 0:
        return tracks.get('items')
    return []


def get_tracks_array(user_id, playlist_name):
    # create array of track objects that only have the necessary information

    tracks = [];
    playlist = get_tracks_from_playlist(user_id, playlist_name)

    if len(playlist) > 0:
        for track in playlist:
            newTrack = {}
            newTrack['name'] = track['track']['name']
            newTrack['artists'] = [name['name'] for name in track['track']['artists']]
            newTrack['popularity'] = track['track']['popularity']
            newTrack['image_url'] = track['track']['album']['images'][1]
            if track['track'].get('preview_url'):
                newTrack['preview_url'] = track['track']['preview_url']
            tracks.append(newTrack)
    
    return tracks

##### RANDOM PLAYLIST FUNCTIONS #####

def get_random_playlists():
    # get playlist objects of the following 11 playlists

    token = get_new_token(client_id, client_secret)

    # generate a list of 11 popular playlists
    playlists = [
        "3ZgmfR6lsnCwdffZUan8EA", "37i9dQZF1DX0XUsuxWHRQd", "5SMf1pyrOAwjwheZvHWkaj", "37i9dQZF1EQpj7X7UK8OOF", "37i9dQZF1EQnqst5TRi17F", 
        "37i9dQZF1DX9qNs32fujYe", "0J74JRyDCMotTzAEKMfwYN", "37i9dQZF1EQqkOPvHGajmW", "1h0CEZCm6IbFTbxThn6Xcs", "01mtswy9f2A3ayUFB2Aynv", "5S8SJdl1BDc0ugpkEvFsIL"
    ]
    random_playlists = []

    # get request to get the tracks in each playlist
    for playlist in playlists:
        response = requests.get(
            f"https://api.spotify.com/v1/playlists/{playlist}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "offset": '0'
            }
        )

        if response:
            response_json = response.json()
            if response_json['tracks']:
                random_playlists.append(response_json)

    return random_playlists 

def get_rand_playlist_tracks(playlist_id):
    # specific function for the largest playlist, which requires multiple requests on the
    # same playlist in order to reach the data point count
    # TODO
    # [ ] do this for all playlists to get every track

    token = get_new_token(client_id, client_secret)

    if playlist_id == "5S8SJdl1BDc0ugpkEvFsIL": # longest playlist, so deal with refresh to get all 10,000 songs
        largest_playlist_obj = {
            "name": "The Longest Playlist on Spotify® (Official)",
            "items": []
        }
        largest_playlist_tracks = []

        # a slight 100 api calls...
        for i in range(0, 100):
            if i % 10 == 0:
                token = get_new_token(client_id, client_secret)
                print(i)
            offset = str(i * 100)
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist_id}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "offset": offset
                }
            )
            if response:
                response_json = response.json()
                largest_playlist_tracks += response_json['tracks']['items']
        largest_playlist_obj['items'] = largest_playlist_tracks
        return largest_playlist_obj

    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "offset": '0'
        }
    )

    json_response = response.json()

    return json_response
     

def get_tracks_from_rand_playlist(playlist_name):
    # get the tracks from the playlist selected

    playlists = get_random_playlists()
    tracks = [];

    for playlist in playlists:
        if playlist['name'] == playlist_name:
            tracks = get_rand_playlist_tracks(playlist['id'])

    # return array of tracks for a particular playlist
    if len(tracks) > 0:
        return tracks.get('items')
    return []

def get_random_tracks_array(playlist_name):
    # get aray of track objects from selected playlist

    tracks = [];
    playlist = get_tracks_from_rand_playlist(playlist_name)

    if len(playlist) > 0:
        print("TRACK #: ", len(playlist))
        for track in playlist:
            newTrack = {}
            newTrack['name'] = track['track']['name']
            newTrack['artists'] = [name['name'] for name in track['track']['artists']]
            newTrack['popularity'] = track['track']['popularity']
            newTrack['image_url'] = track['track']['album']['images'][1]
            if track['track'].get('preview_url'):
                newTrack['preview_url'] = track['track']['preview_url']
            tracks.append(newTrack)
    
    return tracks
