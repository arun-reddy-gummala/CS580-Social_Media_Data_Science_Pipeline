import pymongo
import csv
import unicodecsv
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from unidecode import unidecode
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt

def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)

    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def clean(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", i).split())

pd.set_option("display.max_rows", None, "display.max_columns", None)
cl = pymongo.MongoClient()
db = cl.test
collection = db["twitter"]
covid_1 = collection.find({'data.entities.hashtags.tag' : 'COVID19'},
        {'data.created_at': 1, 'data.text': 1, 'data.source': 1, 'data.public_metrics.retweet_count':1, 'data.favorite_count' : 1, 'data.entities.hashtags': 1
            , 'data.entities.urls' : 1, 'data.entities.media': 1, 'data.entities.user_mentions_data': 1}).limit(8680)

with open('tweets.csv', 'wb') as file:
    writer = unicodecsv.writer(file, delimiter = ',', quotechar = '"')
    writer.writerow(["tweet.create_at", "tweet.text", "tweet.source", "tweet.retweet_count",
                     "tweet_hashtags", "tweet_hashtags_count"])
    for i in covid_1:
        tweet_info = [i["data"]["created_at"], i["data"]["text"], i["data"]["source"],
                  i["data"]["public_metrics"]["retweet_count"]]
        print(tweet_info)
        hashtags = []
        if "hashtags" in i["data"]["entities"]:
            hashtags_data = i["data"]["entities"]["hashtags"]
            if (hashtags_data != None):
                for i in range(len(hashtags_data)):
                    hashtags.append(hashtags_data[i]['tag'])
        print(hashtags)

        more_tweet_info = [', '.join(hashtags),
                       len(hashtags)]
        print(more_tweet_info)
        writer.writerow(tweet_info + more_tweet_info)
df = pd.read_csv("tweets.csv")
df1 = pd.DataFrame()
print(df.head())
print(len(df))
tweets = []
for i in df["tweet.text"]:
    t = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", i).split())
   # t = word_tokenize(t)
    # analysis = get_tweet_sentiment(t)
    tweets_analysis = {}
    tweets_analysis['text'] = t
    tweets_analysis['sentiment'] = get_tweet_sentiment(t)
    if tweets_analysis not in tweets:
        tweets.append(tweets_analysis)
    else:
        tweets.append(tweets_analysis)

# print(tweets)
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
print("Neutral tweets percentage: {} % ".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))
sentiment_objects = [TextBlob(tweet) for tweet in df['tweet.text']]
print(sentiment_objects[1].polarity, sentiment_objects[1])
sentiment_values = [[tweet.sentiment.polarity, str(clean(tweet)), get_tweet_sentiment(str(tweet))] for tweet in sentiment_objects]
sentiment_values[0]
sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet", "sentiment"])
#print(sentiment_df)
fig, ax = plt.subplots(figsize=(8, 6))
# Plot histogram of the polarity values
sentiment_df.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25, 0.5, 0.75, 1],
             ax=ax,
             color="purple")

plt.title("Sentiments from Tweets on COVID19")
plt.xlabel('Polarity value')
plt.ylabel('Tweets')
plt.show()
sentiment_df.sentiment.value_counts().plot(kind='bar', color=["yellow", "green", "red"])
plt.title("Sentimental Analysis on Tweets")
plt.xlabel('Polarity')
plt.ylabel('Tweets')
plt.show()
# airline_sentiment = airline_tweets.groupby(['airline', 'airline_sentiment']).airline_sentiment.count().unstack()
# airline_sentiment.plot(kind='bar')
df['tweet.create_at'] = pd.to_datetime(df['tweet.create_at'], dayfirst=True)
df2 = df.groupby(df['tweet.create_at'].dt.date).size().reset_index(name='Count')
print(df2)
df2.plot(kind='bar', x='tweet.create_at', y='Count')
plt.title('Tweet count on COVID19 per day')
plt.ylabel('Tweets')
plt.show()
df3 = pd.DataFrame()
df3['date'] = df['tweet.create_at']
df3['sentiment'] = sentiment_df['sentiment']
df3['date'] = pd.to_datetime(df3['date'], format='%m/%d/%Y',dayfirst=True)
# df4 = df3.groupby(df3['date', 'sentiment']).df4.count()
# # print(df4)
# df4 =  df3.set_index('date').groupby([pd.Grouper(freq='1440Min'), 'sentiment']).count()
# print(df4)
# df3 = df3.groupby(df3["date"].dt.date)
# df3['sentiment'] = df3['sentiment'].map(map)
df4 = df3.groupby([df3['sentiment'],pd.Grouper(key= 'date', freq='D')]).size()
print(df4)
df4.plot(kind='bar',color=["red", "yellow", "green", "blue", "violet"])
plt.title('Sentimental Analysis on COVID19 tweets per day')
plt.ylabel('Tweets')
plt.show()
# df3.groupby(['date', 'sentiment']).agg('count').reset_index()
# print(df3)
# df4 = df3.groupby([df3['date'].dt.date])
# group = df4["sentiment"].agg(lambda column: column)
# group = group.reset_index(name="sentiment")
# print(group)

