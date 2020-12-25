# TODO: clean up unused imports


# imports here
import json
import os
import re
import sqlite3
import time
from os import getenv

import lyricsgenius
import pandas as pd
import requests
import sqlalchemy
from dotenv import load_dotenv
from flask import flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Lyricly import app, db
from Lyricly.forms import LoginForm, RegistrationForm
from Lyricly.models import Lyrics, Wordcount
from Lyricly.word_count import word_freq

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
        print('query was None')
        load_dotenv()
    
        # API access
        client_access_token = getenv('CLIENT_ACCESS_TOKEN')
        genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                                    skip_non_songs=True, excluded_terms=["Remix", "Live", "Edit", "Mix", "Club"])

        # song search
        search = genius.search_song(data['title'], artist=data['artist'], get_full_info=True)
        
          
        if search is not None:
            insert = Lyrics(search.artist, search.title, search.lyrics)
            db.session.add(insert)
            db.session.commit()
        else:
            # TODO: impliment measures if search is None
            print("search not found")
            
            

    
    query = Lyrics.query.filter_by(artist=data['artist'], title=data['title']).first_or_404()
    print(query.title, 'By:', query.artist)
    
    return jsonify(data)


''' Route that makes a database call to pull lyrics by artist and song title sent from front end
    and analyze word count to be sent back to the front end '''
    
# FIXME: database is not querying certain songs correctly 
# FIXME: rewrite route for better optimization. 

@app.route('/word_count', methods=['POST', 'GET'])
def word_count():
    
    # catch incoming json

    data = request.get_json()
    load_dotenv()
    
    # artist and title stacks
    artist_stack  = []
    title_stack = []
    list = []
    dict = {} 
    
    
    for i in data: 
        artist_stack.append(i['artist'])
        title_stack.append(i['title'])
    
        
    for i in range(len(artist_stack)):
        
        # query the database 
        first_query = Lyrics.query.filter_by(artist=artist_stack[i], title=title_stack[i]).first()
        db.session.commit()
        
        # if the first database query is None, add it to the database
        if first_query is None:
            
            # genius client access token
            client_access_token = getenv('CLIENT_ACCESS_TOKEN')
            genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                                skip_non_songs=True, excluded_terms=[])

            # song search
            search = genius.search_song(title_stack[i], artist=artist_stack[i], get_full_info=True)
            
            if search is not None:
                insert = Lyrics(search.artist, search.title, search.lyrics)
                db.session.add(insert)
                db.session.commit()
            else:
                # TODO: impliment measures if search is None
                print("search not found")    
          
                
        # second query check 
        second_query = Lyrics.query.filter_by(artist=artist_stack[i], title=title_stack[i]).first()
        
        # if second_query is None
        if second_query is None:
            print('\n [///~~~Query of {} By: {} failed~~~///]\n'.format(title_stack[i], artist_stack[i]))
            # TODO: database call to check if lyrics exist, if it doesnt exist, scrape from a different api / page
            continue
        
        # queried lyrics passed through word_freq function
        lyrics = second_query.lyrics
        list = word_freq(lyrics)
        # word_freq output to dictionary 
        key = title_stack[i] + ' By: ' + artist_stack[i]
        dict.setdefault(key, []).append(list)
        print(dict)
    # Dictionary to json object 
    json_object = json.dumps(dict, indent=1)
    return jsonify(json_object)







# TODO: machine learning / AI song generator route 

@app.route('/song_generator', methods=['POST'])
def song_generator():
    pass




# TODO: cosine similarity song suggestor route
@app.route('/song_suggestor', methods=['POST'])
def song_suggestor():
    pass
