import os
import gc
import time
import json
import pandas as pd
import requests_cache
from datetime import datetime
from requests import exceptions
from sqlalchemy import create_engine

import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

"""
Create a SQLAlchemy engine to connect to the MySQL database "music_project" using the PyMySQL driver.
The full connection string (including username, password, host, and database name)
is stored in the environment variable MUSIC_PROJECT_DB_URL.
Example format: "mysql+pymysql://user:password@localhost/music_project"
"""
engine = create_engine(os.getenv("MUSIC_PROJECT_DB_URL"))

# Free memory and clear local request caches between batches.
def run_cleanup():
    # Force Python garbage collection.
    gc.collect()
    # Removes Spotipy .cache file if present (token cache).
    if os.path.exists(".cache"):
        os.remove(".cache")
    # Clears requests_cache global cache (if configured elsewhere).   
    requests_cache.clear()  

#Instantiate a Spotipy client and validate connectivity by calling a known endpoint.
def connect_to_spotify(credential):
    # Build a client with the provided client credentials manager
    sp = spotipy.Spotify(client_credentials_manager = credential)
    try:
        # Lightweight call to verify credentials work
        sp.audio_analysis('spotify:track:5ihS6UUlyQAfmp48eSkxuQ')
        print("Connected to Spotify!")      
    except SpotifyException as e:
        print(f"Error connecting to Spotify: {e.msg}") 
    except Exception as e:
        print(f"Unexpected error: {e}")
    return sp

# Print a simple progress log with elapsed minutes and number of processed items.
def log_progress(key, start_time, passes):
    end_time = time.time()
    elapsed_minutes = round((end_time - start_time) / 60, 2)
    
    print(f"{datetime.now().strftime('%H:%M')} - {key} key ran for {elapsed_minutes} minutes and processed {passes} timbres.")

# Convert a positive integer (1-based) to a base-26 'a'..'z' string.
# Example: 1->'a', 26->'z', 27->'aa'.
# Used to iterate search terms deterministically.
def create_search_term(num):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    term = ''
    while num > 0:
        num -= 1                     # Shift to 0-based for modulo math
        remainder = num % 26         
        term += alphabet[remainder]  # Append current char
        num //= 26                   # Move to next digit
    return term[::-1]                # Reverse to correct order

#Convert a base-26 'a'..'z' string back to its 1-based integer index.
# Inverse of create_search_term.
def term_to_number(term):
    number = 0
    for char in term:
        number = number * 26 + (ord(char) - ord('a') + 1)
    return number

# Look up all previously used search terms in the DB and compute the next term to try.
def get_next_term():
    sql_query = "SELECT DISTINCT search_term FROM tracks"
    search_terms = pd.read_sql(sql_query, con = engine).search_term.tolist()
    
    # First run: start at 'a' with index 1
    if not search_terms:
        return ('a', 1)
    else:
        next_term_num = max([term_to_number(term) for term in search_terms]) + 1
        return (create_search_term(next_term_num), next_term_num)
    
#  Fetch Spotify API credentials from the DB and build a label->SpotifyClientCredentials dict
def get_credentials():
    credential_query = """SELECT * FROM credentials ORDER BY label"""
    credential_df = pd.read_sql_query(credential_query, con = engine)
    credentials = {}
    for index, row in credential_df.iterrows():
        credentials[row['label']] = SpotifyClientCredentials(client_id = row['client_id'],
                                                             client_secret= row['client_secret'])  
    return credentials 

# Search Spotify for tracks matching a given search term.
# Handles 429 (rate limit) distinctly by returning the status code.
def get_tracks(sp, search_term):
    try:
        results = sp.search(f"track:{search_term}", type = 'track', limit = 50)['tracks']['items']
    except SpotifyException as e:
        if e.http_status == 429:  
            # Signal to caller that we hit rate limiting
            return e.http_status
        else:
            print(f"Error for URI {search_term} - HTTP Status: {e.http_status}, Message: {e.msg}")
            return e.http_status
    
    # Normalize empty results to None
    if not results:
        return None
    else:
        return results

"""
Pull distinct track URIs that:
- Have duration between ~1.5 min and ~12.5 min
- Have popularity above the provided threshold
- Do not already have timbre data collected
"""
def get_track_uris(popularity):
    uri_sql_query = f"""SELECT DISTINCT track_uri 
                        FROM tracks
                        WHERE track_duration_ms BETWEEN (1.5*60*1000) AND (15*50*1000)
                             AND popularity > {popularity}
                             AND track_uri NOT IN (SELECT DISTINCT track_uri
                                                   FROM timbres)"""
    track_uris = pd.read_sql_query(uri_sql_query, con = engine).track_uri.tolist()
    return track_uris

# Deduplicate and append new track records to the tracks table.
def append_tracks(tracks, search_term):
    # Get existing URIs for de-duplication
    existing_tracks_query = """SELECT DISTINCT track_uri FROM tracks"""
    existing_track_uris = pd.read_sql(existing_tracks_query, con = engine).track_uri.tolist()
    
    #  Extract fields from API results
    track_uris = [track['id'] for track in tracks]
    track_names = [track['name'] for track in tracks]
    artist_uris = [track['artists'][0]['id'] for track in tracks]
    popularities = [track['popularity'] for track in tracks]
    searched = [search_term] * len(tracks)
    durations = [track['duration_ms'] for track in tracks]
    
    # Build DataFrame for bulk insert
    track_df = pd.DataFrame({'track_uri':track_uris,
                             'track_name':track_names,
                             'artist_uri':artist_uris,
                             'popularity':popularities,
                             'search_term':searched,
                             'track_duration_ms':durations}) 
    
    # Drop any existing URIs
    track_df = track_df[~track_df['track_uri'].isin(existing_track_uris)]
    # Drop duplicates by (track_name, artist_uri) to avoid same track across different releases
    track_df = track_df.drop_duplicates(subset = ['track_name', 'artist_uri'], keep = 'first')
    # Final dedupe on URI, just in case
    track_df = track_df.drop_duplicates(subset = 'track_uri', keep = 'first')
    # Append to DB
    track_df.to_sql('tracks', con = engine, if_exists = 'append', index = False) 
    
    print(f"Term '{search_term}' produced {len(track_df)} new tracks.")
    
    return len(track_df)
  
# Deduplicate and append new artist records to the artists table.   
def append_artists(results):
    
    artist_uri_query = """SELECT DISTINCT artist_uri FROM artists"""
    existing_artist_uris = pd.read_sql(artist_uri_query, con = engine).artist_uri.tolist()
    # Pull primary artist for each track result
    artist_uris = [result['artists'][0]['id'] for result in results]
    artist_names = [result['artists'][0]['name'] for result in results]
    # Create a DF to send to DB
    artist_df = pd.DataFrame({'artist_uri': artist_uris,
                              'artist_name': artist_names})
     # Deduplicate by URI and against existing table      
    artist_df = artist_df.drop_duplicates(subset = 'artist_uri', keep = 'first')
    artist_df = artist_df[~artist_df['artist_uri'].isin(existing_artist_uris)]
    # Append to DB
    artist_df.to_sql('artists', con = engine, if_exists = 'append', index = False)
    print(f"{len(artist_df)} new artists added.")

# Extract and validate timbre data for a track, then append to DB.
def append_timbre(track_uri, segments):
    # Extract timbre arrays from analysis segments
    timbre = [segment['timbre'] for segment in segments]
    # Basic quality/length guardrails (arbitrary thresholds)
    if(len(timbre) < 200 or len(timbre) > 2000):
        print("Track skipped.")
        return
    # Store as JSON string for DB
    timbre = json.dumps(timbre)
    # Create a DF to send to DB
    timbre_df = pd.DataFrame({'track_uri': [track_uri],
                              'track_timbre': [timbre]})
    # Append to DB
    timbre_df.to_sql('timbres', con = engine, if_exists = 'append', index = False)
    
"""
Iterate through credential sets (API keys) to acquire tracks and artists:
      - Rotate keys upon rate-limit or error.
      - Generate deterministic search terms.
      - Append tracks and artists to DB with de-duplication.
"""
def run_track_artist_acquisition(credentials, num_wanted_tracks):
    for key, credential in credentials.items():
        if key == 'alpha':
            continue
        
        print(f"Utilizing key {key}.")
        
        # Clear caches and token files between runs
        run_cleanup()  
        # Connect to Spotify
        sp = connect_to_spotify(credential)
        
        # Determine starting search term from DB history
        next_search_term = get_next_term()
        i = next_search_term[1]

        print(f"Starting at term '{next_search_term[0]}'.")
        
        # Acquire until we hit the target count or rate limit
        while num_wanted_tracks > 0:
            # Generate search term
            search_term = create_search_term(i)
            i += 1
            # Use the search term to retrieve track URIs
            tracks = get_tracks(sp, search_term)
            # Cleanup
            run_cleanup()  
            # If get_tracks returned an int, it's an error code: rotate to next key
            if isinstance(tracks, int):
                print("Next key")
                break
            # No results: move on to next term
            elif not tracks:
                continue
            # Insert tracks and artists; decrement remaining wanted count
            num_tracks_found = append_tracks(tracks, search_term)
            append_artists(tracks)
            num_wanted_tracks -= num_tracks_found
            # Cleanup + pause to avoid rate limit
            run_cleanup() 
            time.sleep(3)
            
"""
Iterate through credential sets (API keys) to fetch timbre for eligible tracks:
- Select track URIs above a popularity threshold without existing timbre.
- For each URI, request audio_analysis and persist timbre segments.
- Rotate keys on 429 or network timeout, logging progress.         
"""
def run_timbre_acquisition(credentials, popularity_min):
    for key, credential in credentials.items():
        # Get list of track URIs to run through
        track_uris = get_track_uris(popularity_min)
        
        # If none left, done
        if not track_uris:
            break
            print(f"All timbres for tracks of popularity {popularity_min} or higher are found.")
        
        print(f"Utilizing key {key}.")
        
        # Cleanup
        run_cleanup()  
        # Connect to Spotify
        sp = connect_to_spotify(credential)
        # Initiate porgress tracking
        passes = 0
        start_time = time.time()
        
        print(f"Running {key} at {datetime.now().strftime('%H:%M')}")
        
        # Process each URI in this batch
        for uri in track_uris:
            try:
                segments = sp.audio_analysis(uri)['segments']
            except SpotifyException as e:
                if e.http_status == 404:
                    # Some tracks have no analysis available
                    print(f"No audio analysis available for URI: {uri}")
                    continue
                elif e.http_status == 429:  
                    # Rate-limited: log and rotate to next key
                    log_progress(key, start_time, passes)
                    break
                else:
                    # Other API errors: log and continue
                    print(f"Error for URI {uri} - HTTP Status: {e.http_status}, Message: {e.msg}")
                    continue
            except exceptions.ReadTimeout:
                # Network timeout: log and rotate to next key
                log_progress(key, start_time, passes)
                break  
            # Persist timbre if acceptable size
            append_timbre(uri, segments)
            # Periodic progress feedback
            passes += 1
            if passes % 50 == 0:
                print(f"Timbres obtained so far: {passes}")
            # Throttle requests to reduce 429s
            time.sleep(7)
        # Encourage freeing network sockets promptly    
        del sp
            

# Get track and artist URIs
run_track_artist_acquisition(get_credentials(), 100000)

# Get timbres
run_timbre_acquisition(get_credentials(), 
                       popularity_min = 60)