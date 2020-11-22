# imports here
import time
import lyricsgenius
import re
import requests
import sqlalchemy
import sqlite3
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

engine = create_engine('sqlite:///songs.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


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
    
    query = Lyrics.query.filter_by(artist=data['artist'], title=data['title']).first()
    
    # if return [] statment
    if query == None:
        load_dotenv()

        # API access
        client_access_token = getenv('CLIENT_ACCESS_TOKEN')
        genius = lyricsgenius.Genius(client_access_token, remove_section_headers=True,
                                     skip_non_songs=True, excluded_terms=["Remix", "Live", "Edit", "Mix", "Club"])

        # song search
        search = genius.search_song(
            data['title'], artist=data['artist'], get_full_info=True)

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
            "Lyricly\songs.db"), if_exists='append', index=False)
        
        query = Lyrics.query.filter_by(artist=data['artist'], title=data['title']).first()

    # send artist name and song name to genius web scraper
    print(query.title,'by:', query.artist)
    return jsonify(data)


'''Route that makes a database call to the lyrics column to pull lyrics and analyze word count to be sent to the front end'''

@app.route('/word_count', methods=['POST'])
def word_count():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    artist = []
    title = []
    lyrics = []
    # iterate through json format
    for i in data:
        artist.append(data[i]['artist']) 
        title.append(data[i]['title'])
    
    for i in range(len(artist)):
        query = Lyrics.query.filter_by(artist=data['artist'], title=data['title']).first()
        
        lyrics.append(query.lyrics)
        # append lyrics to lyrics list
        pass



    pass