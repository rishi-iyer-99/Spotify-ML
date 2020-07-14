import statistics 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from secrets import client_id, client_secret
import json

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


UPDATE_ALL = False
features = ["acousticness","danceability","duration_ms","energy","instrumentalness","key",
			"liveness","loudness","mode","speechiness","time_signature","valence"]

def get_artist_data(artist_id):
	data = dict()
	data["artist_id"] = artist_id
	artist_obj = sp.artist(artist_id)
	data["artist_name"] = artist_obj.get("name")

	top_tracks = sp.artist_top_tracks(artist_id).get("tracks")
	track_ids = []
	for t in top_tracks:
		track_ids.append(t.get("uri"))
	features_list = sp.audio_features(track_ids)

	for f in features:
		stats = get_feature_stats(f, features_list)
		data[f+"_min"] = stats.get("min")
		data[f+"_max"] = stats.get("max")
		data[f+"_avg"] = stats.get("avg")
		data[f+"_std"] = stats.get("std")

	
	data["genres"] = artist_obj.get("genres")
	data["popularity"] = artist_obj.get("popularity")

	return data

def get_feature_stats(feature, features_list):
	stats = dict()
	values = []
	for f in features_list:
		values.append(f.get(feature))


	stats["min"] = min(values)
	stats["max"] = max(values)
	stats["avg"] = sum(values)/float(len(values))
	stats["std"] = statistics.pstdev(values) 
	return stats

def process_artists(artist_ids,old_data):
	if old_data is None:
		data = dict()
	else:
		data = old_data
	for a in artist_ids:
			if (UPDATE_ALL or a not in data.keys()):
				try:
					data[a] = get_artist_data(a)
				except:
					print("Failed to Retrieve Data for {}".format(a))
	print("{} Total Artists Retrieved".format(len(data)))
	return data


def read_json(input_file):
	try:
		with open(input_file) as f:
			data= json.load(f)
		return data
	except:
		return None

def write_json(data,output_file):
	jason = json.dumps(data,indent=4)
	path = output_file
	f = open(path,"w")
	f.write(jason)
	f.close()

#Returns an array of artst ids from txt file
def read_txt(filename):
	with open(filename) as f:
		artists = f.read().splitlines() 
	artist_ids = [str(s) for s in artists]
	return artist_ids

if __name__ == '__main__':
	print("Reading Input Files...")
	artist_ids = read_txt("artists.txt")
	artist_ids = [i for i in artist_ids if i] 
	old_data = read_json("artist_data.json")

	print("Updating Artist Data...")
	artist_data = process_artists(artist_ids, old_data)

	print("Writing Data to JSON...")
	write_json(artist_data, "artist_data.json")

	print("Success")

