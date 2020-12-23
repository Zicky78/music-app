# imports here
import time
import lyricsgenius
import re
import requests
import sqlalchemy
import sqlite3
import os 
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Lyricly.word_count import word_freq
from Lyricly import db
from Lyricly import app
from Lyricly.forms import RegistrationForm, LoginForm
from Lyricly.models import Lyrics, Wordcount
from os import getenv
from dotenv import load_dotenv
from flask import render_template, url_for, flash, redirect, jsonify, request
import pandas as pd
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


# Session Engine
# TODO: Rewrite for clean up and optimization 
@app.route('/song', methods=['POST'])
def song_search():
    print("Incoming...")
    # recieve artist name / song namr in json format
    data = request.get_json()
    print(request.get_json())
    artist = data['artist']
    title = data['title']
    query = Lyrics.query.filter_by(artist = artist, title= title).first()
    db.session.commit()
    # if return [] statment
    if query == None:
        print('query was Joe Biden')
        load_dotenv()
    
        # API access
        client_access_token = getenv('CLIENT_ACCESS_TOKEN')
        genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                                    skip_non_songs=True, excluded_terms=["Remix", "Live", "Edit", "Mix", "Club"])

        # song search
        search = genius.search_song(data['title'], artist=data['artist'], get_full_info=True)
        
        # list for database conversion
        artist = []
        name = []
        lyrics = []
        artist.append(search.artist)
        name.append(search.title)
        lyrics.append(search.lyrics)

        tracklist = pd.DataFrame(
            {'artist': artist, 'title': name, 'lyrics': lyrics})

        tracklist.to_sql("lyrics", sqlite3.connect(
            "Lyricly\songs.sqlite3"), if_exists='append', index=False)
        

    
    query = Lyrics.query.filter_by(artist=data['artist'], title=data['title']).first_or_404()
    print(query.title, 'By:', query.artist)
    
    return jsonify(data)


''' Route that makes a database call to pull lyrics by artist and song title sent from front end
    and analyze word count to be sent back to the front end '''
    
# FIXME: database is not querying certain songs correctly 
# FIXME: rewrite entire route for better optimization. 

@app.route('/word_count', methods=['POST'])
def word_count():
    
    # catch incoming json

    data = request.get_json()
    load_dotenv()
    
    # artist and title stacks
    artist_stack = []
    title_stack = []
    list = []
    dict = {} 
    
    for i in data: 
        artist_stack.append(i['artist'])
        title_stack.append(i['title'])
    
    #     
    for i in range(len(artist_stack)):
        first_query = Lyrics.query.filter_by(artist=artist_stack[i], title=title_stack[i]).first()
        db.session.commit()
        if first_query is None:
            
            
            client_access_token = getenv('CLIENT_ACCESS_TOKEN')
            genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                                skip_non_songs=True, excluded_terms=[])

            # song search
            search = genius.search_song(title_stack[i], artist=artist_stack[i], get_full_info=True)
            
            # list for database conversion
            artist = []
            title = []
            lyrics = []
            artist.append(search.artist)
            title.append(search.title)
            lyrics.append(search.lyrics)
            tracklist = pd.DataFrame({'artist': artist, 'title': title, 'lyrics': lyrics})
            tracklist.to_sql("wordcount", sqlite3.connect("Lyricly\songs.sqlite3"), if_exists='replace', index=True, index_label='id')
                
        
        second_query = Wordcount.query.filter_by(artist=artist_stack[i], title=title_stack[i]).first()
        
        if second_query is None:
            print('\n [///~~~Query of {} By: {} failed~~~///]\n'.format(title_stack[i], artist_stack[i]))
            # TODO: database call to check if lyrics exist, if it doesnt exist, scrape from a different api / page
            continue
            
        lyrics = second_query.lyrics
        list = word_freq(lyrics)
        
        key = title_stack[i] + ' By: ' + artist_stack[i]
        dict.setdefault(key, []).append(list)
    
    json_object = json.dumps(dict, indent=1)
    print(json_object)
    return jsonify(json_object)







# TODO: machine learning / AI song generator route 

@app.route('/song_generator', methods=['POST'])
def song_generator():
    pass




# TODO: cosine similarity song suggestor route
@app.route('/song_suggestor', methods=['POST'])
def song_suggestor():
    pass
