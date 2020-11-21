
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
    print(unfiltered_lyrics)
    # tokenize lyrics
    unfiltered_lyrics = re.sub('[^a-zA-Z ]', '', unfiltered_lyrics[0])
    unfiltered_lyrics = unfiltered_lyrics.lower().split()
    # filter out pre-set stop words
    stop_words = set(stopwords.words("english"))
    filtered_lyrics = []
    for x in unfiltered_lyrics:
        if x not in stop_words:
            filtered_lyrics.append(x)
    # get word frequency of document 
    fdist = FreqDist(filtered_lyrics)

    return fdist.most_common(15)

lyrics  = "I was fifteen when the world put me on a pedestal I had big dreams of doin' memories, memories, memories, shows and making memories Made some bad moves tryna act cool, upset by their jealousy And now I really wanna know"

print(word_freq(lyrics))