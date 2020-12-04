
from Lyricly import db

# User table 
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
    
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Lyrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    lyrics = db.Column(db.Text)
    # save document vectors to the database
    
    
    def __repr__(self):
        return f"lyrics('{self.artist}', '{self.title}', '{self.lyrics}')"