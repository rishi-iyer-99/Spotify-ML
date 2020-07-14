import statistics 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from secrets import client_id, client_secret

cid =client_id # Client ID; copy this from your app 
secret = client_secret # Client Secret; copy this from your app
username = 'Rishi Iyer' # Your Spotify username

#for avaliable scopes see https://developer.spotify.com/web-api/using-scopes/
scope = 'user-library-read playlist-modify-public playlist-read-private'
redirect_uri='http://localhost:8888/callback' # Paste your Redirect URI here
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
token = util.prompt_for_user_token(username, scope, cid, secret, redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)


#Returns an array of artst ids from txt file
def read_txt(filename):
	with open(filename) as f:
		playlists = f.read().splitlines() 
	playlist_ids = [str(s) for s in playlists]
	return playlist_ids

def write_txt(data, filename):
	with open(filename, 'w') as filehandle:
		for listitem in data:
			filehandle.write('%s\n' % listitem)

def read_playlist(playlist_id):
	artist_ids = set()
	tracks = sp.playlist_tracks(playlist_id).get("items")
	for t in tracks:
		artists= t.get("track").get("artists")
		for a in artists:
			artist_ids.add(a.get("id"))
	return artist_ids

def process_playlists(playlist_ids):
	artist_ids = set()
	for p in playlist_ids:
		artist_ids.update(read_playlist(p))
	return artist_ids


if __name__ == '__main__':
	print("Reading Input..")
	playlist_ids = read_txt("playlists.txt")
	old_artists = read_txt("artists.txt")
	print("Getting IDs...")
	artist_ids = process_playlists(playlist_ids)
	artist_ids.update(old_artists)
	print("Writing to txt...")
	write_txt(artist_ids,"artists.txt" )