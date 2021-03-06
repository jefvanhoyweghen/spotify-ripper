import spotipy.util as util
import spotipy.client
import os

redirect_uri = 'http://www.purple.com'
client_id = ''
client_secret = ''
scope = 'playlist-modify-public playlist-modify-private playlist-read-collaborative'

# client_id = os.environ["SPOTIPY_CLIENT_ID"]
# client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
# redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

token = None
spotInstance = None


def remove_all_from_playlist(username, playlistURI):
    tracks = get_playlist_tracks(username, playlistURI)

    track_ids = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        tid = track['id']
        track_ids.append(tid)
    results = spotInstance.user_playlist_remove_all_occurrences_of_tracks(username, rPlaylistID, track_ids)


def get_playlist_tracks(username, playlistURI):
    global rPlaylistID
    p1, p2, p3, p4, rPlaylistID = playlistURI.split(':', 5)

    global token
    token = util.prompt_for_user_token(username, scope)

    global spotInstance
    spotInstance = spotipy.Spotify(auth=token)
    spotInstance.trace = False

    offset = 0
    tracks = []
    next = True

    print('Getting Results')
    while next != None:
        results = spotInstance.user_playlist_tracks(username, rPlaylistID, fields="items,total,next", limit=100, offset=offset)
        tracks.extend(results['items'])
        offset = offset + 100
        next = results['next']

    return tracks
