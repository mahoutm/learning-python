# Get Timeline Tweets with OAuth Authorization
import tweepy

consumer_key = '<INPUT C KEY>'
consumer_secret = '<INPUT CS KEY>'

access_token = '<INPUT TOKEN>'
access_token_secret = '<INPUT S TOKEN>'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text
