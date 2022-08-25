# Real Time Twitter Sentiment Analysis
A collaborative work of Umaima Siddiqua and Syeda Fatima Ali

## Abstract

  Sentiment analysis alludes to the application for processing natural language, 
text analysis, computational linguistics, and biometrics to methodically recognize, 
extract, quantify, and learn affective states and subjective information in source 
material. Twitter, being one among several popular social media platforms, is a place 
where people often choose to express their emotions and sentiments about a brand, a 
product or a service. Analysing sentiments for tweets is very helpful in determining 
people's opinion as positive, negative or neutral. This thesis evaluates a person’s 
tweets to know whether he/she builds a positive or negative impact on people. Twitter 
API is used to access the tweets directly from twitter and build a sentiment 
classification for the tweets. The outcome of the analysis is depicted for positive, 
negative and neutral remarks about their opinions using visualization techniques such 
as a histogram and a wordcloud.

## Algorithm Description

### 1. Authenticate Twitter Account
Authentication of Tweepy tool from the developers section of twitter website
```python
consumer_key = ‘xxxxxxx'
consumer_secret = ‘xxxxxxx'
access_token = ‘xxxxxx'
access_token_secret = ‘xxxxxx’

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
```

### 2. GET Request
 This request is made to twitter for getting access to tweets
```python
 # Extract 100 tweets from the twitter user
posts=api.user_timeline(
	screen_name=raw_text,
	count = 100,
	lang ="en",
	tweet_mode="extended“)
```

### 3. Perform Sentiment Analysis
The sentiment classifier functions divides the tweets as positive, negative and neutral based on the polarity in the range -1.0 to 1.0

```python
# Create a function to get the subjectivity
def getSubjectivity(text):
      return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
      return  TextBlob(text).sentiment.polarity
```

## Conclusion
Towards a Better Living!

In today's world, violent content is spreading across Twitter and is usually targets a particular community, government, religion, celebrities or politicians.
The aim of this project is to counter this violent extremism and it's spread  on Twitter. 
This project is able to provide a real-time sentiment analysis of any community, government, religion, celebs or politicians across the global anytime using lexical resources.
