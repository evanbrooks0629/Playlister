from http.client import HTTPResponse
import json
from flask import Flask, redirect, url_for, render_template, request
from spotify import *
from linked_list import DoublyLinkedList
from shuffle import *
from graph import Graph
from heap import Min_Heap

app = Flask(__name__, static_folder="./static")

# user_data object, used to store session data between requests
user_data = {
    'username': 'User',         # used to let them access their playlists
    'playlists': [],            # users playlists
    'rand_playlists': [],       # preselected set of random playlists, including one with 10,000 tracks
    'playlist': 'No Playlist',  # selected playlist
    'tracks': [],               # tracks in selected playlist
    'tracks_dll': None,         # doubly linked list of tracks
    'tracks_heap': None,        # heap of tracks
    'index': 0                  # playback position in tracks
}

@app.route("/", methods=["POST", "GET"])
def home():
    rand_playlists=get_random_playlists()
    user_data['rand_playlists'] = rand_playlists

    # gets every action from the user sent with certain data
    if request.method == "POST":
        if 'username' in request.form:
            username = request.form['username']
            user_data['username'] = username

            # get user's playlists
            playlists=get_users_playlists(username)
            user_data['playlists'] = playlists
            user_data['playlist'] = 'No Playlist'
            user_data['tracks'] = []
            user_data['index'] = 0

        # SELECT PLAYLIST

        if 'select_playlist' in request.form:
            user_data['playlist'] = request.form['select_playlist']
            
            # GET ARRAY OF TRACKS WHEN USER SELECTS PLAYLIST
            # TURN INTO A DOUBLY LINKED LIST

            playlist_tracks_array = get_tracks_array(user_data['username'], user_data['playlist']) 
            tracks_dll = DoublyLinkedList()
            tracks_dll.read_array(playlist_tracks_array)

            user_data['tracks'] = playlist_tracks_array
            user_data['tracks_dll'] = tracks_dll
            user_data['index'] = 0

        if 'select_random_playlist' in request.form:
            user_data['playlist'] = request.form['select_random_playlist']

            # GET ARRAY OF TRACKS WHEN USER SELECTS PLAYLIST
            # TURN INTO A DOUBLY LINKED LIST

            playlist_tracks_array = get_random_tracks_array(user_data['playlist'])
            tracks_dll = DoublyLinkedList()
            tracks_dll.read_array(playlist_tracks_array)

            user_data['tracks'] = playlist_tracks_array
            user_data['tracks_dll'] = tracks_dll
            user_data['index'] = 0

        # PLAYBACK BUTTONS

        if 'submit_shuffle' in request.form:
            if len(user_data['tracks']) > 0:
                shuffled_playlist = fisher_yates(user_data['tracks'])
                user_data['tracks'] = shuffled_playlist
                user_data['index'] = 0

        if 'submit_p_shuffle' in request.form:
            if len(user_data['tracks']) > 0:
                shuffled_playlist = psuedo_shuffle(user_data['tracks'])
                user_data['tracks'] = shuffled_playlist
                user_data['index'] = 0

        if 'submit_f_t_b' in request.form:
            # get forward array from LL, set tracks to it

            if len(user_data['tracks']) > 0:
                user_data['index'] = 0
                tracks_dll = user_data['tracks_dll']
                user_data['tracks'] = tracks_dll.get_forward_array()

        if 'submit_b_t_f' in request.form:
            # get backward array from LL, set tracks to it

            if len(user_data['tracks']) > 0:
                user_data['index'] = 0
                tracks_dll = user_data['tracks_dll']
                user_data['tracks'] = tracks_dll.get_backward_array()

        # MUSIC CONTROLS

        if 'forward_button' in request.form:
            # move forward 1 position in tracks
            user_data['index'] += 1    

        if 'back_button' in request.form:
            # move backward 1 position in tracks
            user_data['index'] -= 1   

        if 'done' in request.form:
            # move forward 1 position in tracks if track ends
            user_data['index'] += 1
        
        # return the username to display it
        # call function from spotify to get their available playlists

    # render html template on every change
    return render_template("index.html", username=user_data['username'], playlists=user_data['playlists'], rand_playlists=user_data['rand_playlists'], playlist=user_data['playlist'], tracks=user_data['tracks'], index=user_data['index'])


if __name__ == '__main__':
    app.run(debug=True)
