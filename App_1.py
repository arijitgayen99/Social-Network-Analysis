from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

import twitter_acc
#Python file storing the twitter account access credentials

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_acc.API_KEY, twitter_acc.API_SECRET_KEY)
        auth.set_access_token(twitter_acc.ACCESS_TOKEN, twitter_acc.ACCESS_SECRET_TOKEN)
        return auth




class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = Listener(fetched_tweets_filename)
        auth = TwitterAuthenticator().authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)

class Listener(StreamListener):
    
    def __init__(self, tweet_filename):
        self.tweet_filename = tweet_filename
    
    def on_data(self, data):
        
        try:
            print(data)
            with open(self.tweet_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error is: %s" % str(e))
        return True
        
        
    def on_error(self, status):
        if status == 420:
            return False
        print(status)
        
        
if __name__ == "__main__":
    hash_tag = []
    tweet_filename = "tweets.txt"
    
    print("1. Stream Live tweets via keywords")
    print("2. Extract tweets from a particular user")
    print("3. Exit")
    print("Enter choice: ",end=" ")
    ch = int(input())
    
    if ch == 1:
        num = int(input("Enter number of keywords: "))
        for i in range(num):
            s = input("Enter keyword: ")
            hash_tag.append(s)
        stream = TwitterStreamer().stream_tweets(tweet_filename, hash_tag)
        
    elif ch == 2:
        user = input("Enter username: ")
        num = int(input("Enter number of tweets to return: "))
        gets = TwitterClient(user)
        print(gets.get_user_timeline_tweets(num))

        num = int(input("Enter number of friends: "))
        print("Friend List of ",user," : ")
        print(gets.get_friend_list(num))

    twitter_client = TwitterClient('pycon')
    whatIGot = twitter_client.get_user_timeline_tweets(1)
    print(whatIGot)
    print(type(whatIGot))