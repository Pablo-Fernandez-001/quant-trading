# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 00:02:24 2026

@author: pabda
"""

#import libs
import pandas as pd
import nltk
import string
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # pip install vaderSentiment - conda install vaderSentiment

# Load movies opinions
path = "../data/Output.csv"
df = pd.read_csv(path)
print(f"Data Frame: {df.head()}")
print(f'Sentiment: {df["sentiment"].value_counts()}')

#Tokenizen
tokens_review = [nltk.tokenize.word_tokenize(text.lower()) for text in df["review"]]
print(f"First tokenized review: {tokens_review[0]}")

#Tokenization
lemmatizer = nltk.stem.WordNetLemmatizer()
lemmatizer_tokens_review = [[lemmatizer.lemmatize(token) for token in review] for review in tokens_review]
print(f"Lematization of the first review {lemmatizer_tokens_review[0]}")

#Stemming
stemmer = nltk.stem.PorterStemmer()
stemmed_tokens_review = [[stemmer.stem(token) for token in review] for review in lemmatizer_tokens_review]
print(f"Stemming for firste review {stemmed_tokens_review[0]}")

#Stopwords elimination
stop_words = set(nltk.corpus.stopwords.words("english"))
filtered_tokens_review = [[token for token in review if token not in stop_words] for review in stemmed_tokens_review]
print(f"Token without stopwords for first review {filtered_tokens_review[0]}")

#Normalization
normalizated_review_token = [[token for token in review if token not in string.punctuation] for review in filtered_tokens_review]
print(f"Normalized tokens for first review: {normalizated_review_token[0]}")

#Merge reviews
procesed_text = [" ".join(review) for review in normalizated_review_token]
print(f"First review procesed: {procesed_text[0]}")

# Create an analyzer instance
sia = SentimentIntensityAnalyzer()

# Get sentiment
review_sentiment = [sia.polarity_scores(review) for review in procesed_text]
print(f"Reviews {review_sentiment[:5]}")

# Calificates like "Positive" or "Negative"
general_sentiment = ["positive" if i["compound"] >= 0 else "negative" for i in review_sentiment]
# Add to dataframe
df["Predictions"] = general_sentiment

#Accuracy
# If the review it's long that difficults the model to the accuracy, vader works better with short reviews
accuracy= (df["sentiment"] == df["Predictions"]).mean()
print(f"Text processing with accuracy: {accuracy}")

# Predict with the internal vader's processing
df["Predictions 2"] = df["review"].apply(lambda x: "positive" if sia.polarity_scores(x)["compound"] >= 0 else "negative")
accuracy2 = (df["sentiment"] == df["Predictions 2"]).mean()
print(f"Precition with Vaders's text processing: {accuracy2}")

# Reminder:
#   - Sentiment analysis helps us better understand opinions on various public issues.