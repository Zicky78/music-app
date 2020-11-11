from flask import Flask
from os import getenv
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from Lyricly.forms import RegistrationForm, LoginForm

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = getenv('USER_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

from Lyricly import routes