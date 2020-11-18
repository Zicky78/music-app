from os import getenv
from dotenv import load_dotenv
import pandas as pd
import time
import lyricsgenius
import re
import sqlite3 

load_dotenv()

client_access_token = getenv('CLIENT_ACCESS_TOKEN')
genius = lyricsgenius.Genius(client_access_token, timeout=60, remove_section_headers=True,
                 skip_non_songs=True, excluded_terms=["Remix", "Live", "Edit", "Mix", "Club", "Commentary", "Demo"])


sample_artists = ['Marshmello']
                #   'Red Hot Chili Peppers','Lynyrd Skynyrd','Sheryl Crow','Glint', 'Mike Mains and The Branches',
                #   'Frank Sinatra', 'Spoon', 'The Fray', "Jed's A Millionaire", 'Nano', 'Oral Cigarettes','One OK Rock',
                #   'Sangatsu no Phantasia','Roddy Rich', 'Juice WRLD' ]

# Names ready to be Q'd
'''         
            
'''
#Starting the song search for the artists in question and seconds count
query_number = 0
time1 = time.time()
artists = []
titles = []
lyrics = []
for artist in sample_artists:
    query_number += 1
    #Empty lists for artist, title, album and lyrics information
    print('\nQuery number:', query_number)
    #Search for max_songs = n and sort them by popularity
    artist = genius.search_artist(artist, sort='popularity')
    songs = artist.songs
    song_number = 0
    #Append all information for each song in the previously created lists
    for song in songs:
        if song is not None:
            song_number += 1
            print('\nSong number:', song_number)
            print('\nNow adding: Artist')
            artists.append(song.artist)
            print('Now adding: Title')
            titles.append(song.title)
            print('Now adding: Lyrics')
            lyrics.append(song.lyrics)
    time2 = time.time()
    print('\nQuery', query_number, 'finished in', round(time2-time1,2), 'seconds.')
    
    #Create a dataframe for our collected tracklist   
tracklist = pd.DataFrame({'artist':artists, 'title':titles, 'lyrics':lyrics})   
time3 = time.time()   
print('\nFinal tracklist of', query_number, 'artists finished in', round(time3-time1,2), 'seconds.')
#Save the final tracklist to csv format
tracklist.to_sql("lyrics", sqlite3.connect("songs.db"), if_exists='append', index=False)