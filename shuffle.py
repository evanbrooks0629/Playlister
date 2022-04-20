"""
---PLAN---
>   calculate value given: artist density of the song, popularity && correlation 
    with the song at pivot position
>   track-artist data in a graph to determine artist density + correlation
>   quicksort: the highest value are the ones with higher correlation
*** In case with many data points, keep the sample data to a 
"""

# FUNCTION: create graph (x: artists, y: tracks)
# NOTE: tracks are referred to by IDs (their index)

# CLASS: Track Criteria
# FUNCTION: artist density calculatiion
# FUNCTION: get popularity (EASY -> just extract from track list)
# FUNCTION: correlation to startings point (same artist?, popularity?)
# This is the function that will indicate how we sort things out

# FUNCTION: random seed

# MIN_HEAP:
# generate list of tracks(ID) to be played

# NOTE: No modifications to array, only refer to index to avoid any resizing, reallocation

import random as rand
from random import randrange, sample
# from sample import playlist
from heap import *
from graph import *


""" SHUFFLE FUNCTIONS """

# Fisher-Yates


def fisher_yates(bucket):
    size = len(bucket)
    for x in range(0, size - 1):    # range [x, y)
        j = rand.randint(x, size - 1)    # randint [x, y]
        bucket[x], bucket[j] = bucket[j], bucket[x]
    return bucket


""" HELPER FUNCTIONS """

# Modify Playlist


def mod_playlist(playlist):
    # mod_playlist = []
    popularity = []
    for track in playlist:
        # new_track = {}
        # new_track['name'] = track['name']
        # new_track['image_url'] = track['image_url']
        # new_track['preview_url'] = track['preview_url']
        # new_track['popularity'] = track['popularity']
        popularity.append(track['popularity']/100)
        # mod_playlist.append(track['artists'])
    return playlist, popularity



def psuedo_shuffle(original_playlist):
    playlist = original_playlist
    shuffled = []
    if len(playlist) > 100:
        seed = list(range(0, 100))
    else:
        seed = list(range(0, len(playlist)))
    fisher_yates(seed)
    mod, popularity = mod_playlist(playlist)
    g = Graph(mod, popularity)
    corr = g.get_correlation(seed[0])
    # heap sort
    heap = Min_Heap(g.total_track)
    for item in corr:
        heap.insert(item)
    for j in range(g.total_track):
        tmp, index = heap.pop()  # return score, index
        shuffled.append(index)

    for i, index in enumerate(shuffled):
        playlist[i] = original_playlist[index]
    return playlist
# Example:

"""
HOW-TO
1. get 'playlist' and 'popularity' from mod_playlist(input)
2. create an array of int, shuffle using fisher_yates() to generate random seed
3. create a graph using (inputs are playlist & popularity)
4. use get_correlation with the input of seed
5. create min heap with the size of the playlist
6. insert score array in min heap
"""


# playlist, popularity = mod_playlist(playlist)

# seed = list(range(0, 100))
# fisher_yates(seed)
# print(seed)
# g = Graph(playlist, popularity)
# corr = g.get_correlation(seed[4])  # input base index

# # Min_heap uses
# heap = Min_Heap(g.total_track)

# for item in corr:
#     heap.insert(item)

# shuffled = []
# data = []
# for j in range(g.total_track):
#     tmp, index = heap.pop()  # return score, index
#     shuffled.append(index)
#     data.append(tmp)
# print(shuffled[3])  # shuffled index