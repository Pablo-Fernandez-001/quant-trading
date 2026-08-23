# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 13:30:44 2026

@author: pabda
"""

#import libs
import nltk # pip install nltk - conda install nltk 
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # pip install vaderSentiment - conda install vaderSentiment

# Download necesary resources from NLTK
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# Example text
text = "Cats love to play with small balls! they are playful and energetic."

# First phase, tokenization: Divides the text in smallest units (tokens), generally those are words
tokens = nltk.tokenize.word_tokenize(text.lower())
print(f"Tokens: \n{tokens}\n")

# Second phase, Lematization: Reduces the words to a base for or watchword. For example, "cats" it converts into "cat"
lematizer = nltk.stem.WordNetLemmatizer()
lematized_tokens = [lematizer.lemmatize(token) for token in tokens]
print(f"Lematization: \n{lematized_tokens}\n")

# Third phase, Steamming: Reduces the words into his roots. For example, "playful" it's "play"
stemmer = nltk.stem.PorterStemmer()
stemed_tokens = [stemmer.stem(token) for token in lematized_tokens]
print(f"Stemming: \n{stemed_tokens}\n")

# Forth phase, Stop Words Elimination: Deletes the common words who doesn't gives a lot of sence ("ins", "is", "the")
stop_words = set(nltk.corpus.stopwords.words("english")) # we uses set to uses unique words, or uses once all repeted words
filltered_tokens = [token  for token in stemed_tokens if token not in stop_words]
print("Tokens without stop words: \n{filltered_tokens}\n")

# Fifth phase, Normalization (deleting punctuation symbols): Cleans all text eliminating punctuation, emojies and another non wished special characters
normalized_tokens = [token for token in filltered_tokens if token not in string.punctuation]
print(f"Normalizated Tokens: \n{normalized_tokens}\n")


# Mergin all tokens again in a sentence
processed_text = " ".join(normalized_tokens)
print(f"Processed Text: \n{processed_text}\n")

# Creates the Instance Analyzing the Sentiment
sia = SentimentIntensityAnalyzer()

#Get Sentiment
scores = sia.polarity_scores(processed_text)
print(f"Scores: \n{scores}\n")

#Validate the Sentiment
if scores["compound"] >= 0:
    print("The phrase has a Positive Sentiment!")
else:
    print("The phrase has a Negative Sentiment!")
    
    
# Analyze the text without  own preprocessing
sent_no_processed = sia.polarity_scores(text)
print(f"\nNon processed text: \n{sent_no_processed}\n")

#Validate the Sentiment
if sent_no_processed["compound"] >= 0:
    print("The phrase has a Positive Sentiment!")
else:
    print("The phrase has a Negative Sentiment!")

# Reminder:
#   - Sentiment analysis requires proper text processing to yield accurate results.
#   - Sentiment analysis helps us understand the opinions expressed in the text by providing probabilities
#     regarding how people feel about a specific topic.
