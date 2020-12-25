# TODO: Implement Doc2Vec model on song lyrics from songs chosen by user

import os
import gensim
import sqlite3
import pandas as pd
from Lyricly import app, db
from dotenv import load_dotenv
from Lyricly.models import Lyrics
from Lyricly.forms import RegistrationForm, LoginForm


# sql to DataFrame

conn = sqlite3.connect("songs.sqlite3")
df = pd.read_sql("Select * from Lyrics", conn)


    # import sql database as dataframe

# 