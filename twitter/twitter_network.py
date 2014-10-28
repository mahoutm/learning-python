# Get Timeline Tweets with OAuth Authorization
import tweepy

consumer_key = '<INPUT>'
consumer_secret = '<INPUT>'

access_token = '<INPUT>'
access_token_secret = '<INPUT>'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

lv_list = []
lv_from = []
lv_to = []

for follower in tweepy.Cursor(api.followers,screen_name='sunhee26').items(10):
	lv_list.append(follower.screen_name)

for follower1 in lv_list:
	for follower2 in tweepy.Cursor(api.followers,screen_name=follower1).items(10):
		lv_from.append(follower1)
		lv_to.append(follower2.screen_name)

import numpy as np

lv_mat = np.column_stack((lv_from,lv_to))

print lv_mat

##Load package
#library(igraph)
##relations is data.frame(from=X,to=Y)
#g <- graph.data.frame(relations, directed=F)
#plot(g)
