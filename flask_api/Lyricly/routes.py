from flask import render_template, url_for, flash, redirect
from Lyricly import app
from Lyricly.forms import RegistrationForm, LoginForm
from Lyricly.models import Lyrics
   
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title= 'Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title= 'Login', form=form)
