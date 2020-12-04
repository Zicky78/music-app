
# imports 
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# regex for puctuation removal 
def tokenize(text):
    tokens = re.sub('[^a-zA-Z ]', '', text)
    tokens = tokens.lower().split()
    return tokens

# create function that tokenizes words
def word_freq(lyrics):
    unfiltered_lyrics = []
    unfiltered_lyrics.append(lyrics)
    no_newline_lyrics = " ".join(unfiltered_lyrics[0].split("\n"))
    
   
    # tokenize lyrics
    no_newline_lyrics = re.sub('[^a-zA-Z ]', '', no_newline_lyrics)
    no_newline_lyrics = no_newline_lyrics.lower().split()
    # filter out pre-set stop words
    stop_words = set(stopwords.words("english"))
    filtered_lyrics = []
    for x in no_newline_lyrics:
        if x not in stop_words:
            filtered_lyrics.append(x)
    # get word frequency of document 
    fdist = FreqDist(filtered_lyrics)

    return fdist.most_common(10)