import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from track import Track
import sys
import traceback

SPOTIPY_CLIENT_ID = "SPOTIPY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET = "SPOTIPY_CLIENT_SECRET"

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                                         client_secret=SPOTIPY_CLIENT_SECRET))


def search(query, ff=0, query_type='track'):
    try:
        results = sp.search(q=query, limit=50, type=query_type, offset=ff)
        if len(results[query_type + 's']['items']) > 0:
            if query_type == 'track':
                # return [Track(results[query_type + 's']['items'][0])]
                return results[query_type + 's']['items']
            elif query_type == 'album':
                return pack_album(sp.album(results['album' + 's']['items'][0]['id']))
            elif query_type == 'playlist':
                return pack_playlist(sp.playlist(results['playlist' + 's']['items'][0]['id']))
        else:
            return None
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        from bot import Bot
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def link(query):
    try:
        try:
            if '/track/' in query:
                return [Track(sp.track(query))]
            elif '/album/' in query:
                return pack_album(sp.album(query))
            elif '/playlist/' in query:
                return pack_playlist(sp.playlist(query))
            else:
                return None
        except spotipy.exceptions.SpotifyException:
            return None
    except Exception:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        from bot import Bot
        Bot(None).sendMessage(text=str(tbinfo) + "\n" + str(sys.exc_info()[1]))


def pack_album(album):
    tracks = []
    for track in album['tracks']['items']:
        track_data = track
        track_data['album'] = album
        tracks.append(Track(track_data))
    return tracks


def pack_playlist(playlist):
    tracks = []
    for track in playlist['tracks']['items']:
        track_data = track['track']
        track_data['playlist'] = playlist['name']
        tracks.append(Track(track_data))
    return tracks
