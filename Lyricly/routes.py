# imports here
import time
import lyricsgenius
import re
import requests
import sqlalchemy
import sqlite3
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Lyricly.word_count import word_freq
from Lyricly import db
from Lyricly import app
from Lyricly.forms import RegistrationForm, LoginForm
from Lyricly.models import Lyrics
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


''' Route that makes a database call to the lyrics column to pull lyrics and analyze word count to be sent to the front end '''
# FIXME: database is not querying certain songs correctly 
# FIXME: rewrite entire route for optimization. 

@app.route('/word_count', methods=['POST'])
def word_count():
    # catch incoming json
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    print(data[0]['artist'])
    print(data[0]['title'])
    # lists 
    band = []
    name = []
    words = []
    list = []
    dict = {}
    # iterate through json format
    for i in data:
        band.append(i['artist'])
        name.append(i['title'])
    for i in range(len(band)):
        # artist and song title at the index of i
        a = band[i]
        t = name[i]
        # query to check databse for song
        query = Lyrics.query.filter_by(artist=band[i], title=name[i]).first()
        print(query)
        db.session.commit()
        
        # if the query of a song from database results in None
        if query == None:
            print('Query of {} By: {} resulted in None'.format(t, a))
            load_dotenv()
            # API access
            client_access_token = getenv('CLIENT_ACCESS_TOKEN')
            genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                                    skip_non_songs=True, excluded_terms=[])

            # song search
            search = genius.search_song(t, artist=a, get_full_info=True)
            print(search)
            # list for database conversion
            artist = []
            title = []
            lyrics = []
            artist.append(search.artist)
            title.append(search.title)
            lyrics.append(search.lyrics)

            tracklist = pd.DataFrame(
                {'artist': artist, 'title': title, 'lyrics': lyrics})

            tracklist.to_sql("lyrics", sqlite3.connect(
            "Lyricly\songs.sqlite3"), if_exists='append', index=False)
            
            # song name dictionary with word_freq tuple values
        
        new_query = Lyrics.query.filter_by(artist=band[i], title=name[i]).first()
        print(new_query)
        db.session.commit()
        # tuple list 
        lyrics = new_query.lyrics
        list = word_freq(lyrics)
        
        key = name[i] + ' By: ' + band[i]
        dict.setdefault(key, []).append(list)
        print(dict)
    #         # tuple list
    #         lyrics = query.lyrics
    #         list = word_freq(lyrics)
    #         print(list)
            
    #         return "~~~~~~~~~~"
    #         # for loop to pass lyrics through function with key value of artist and song name
    return "~~~~~~~~~~"
