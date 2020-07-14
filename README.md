# Spotify-ML
This is the code used to fetch artist data using Spotify's API, then apply regression techniques to discover artists that have potential
for growth in popularity but currently have few listeners.  
The repo contains:

 - `scrapeArtists.py`: takes an input file `playlists.txt` that contains playlist ids of playlists of interest, and outputs `artists.txt`, a file containig the artist ids of all artists featured in the playlists
 - `scrapeData.py`: takes input file `artists.txt`, retireves relevant information about the artist's audio features using Spotipy, and saves the dict containing info to `artist_data.json`
 - `SpotifyAnalyis.ipynb`: reads in `artist_data.json` as a table, predicts artist popularity with a Random Forest Regressor, and discovers artists with potential as those with the highest difference between predicted and actual popularity in the test set.
