from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import numpy as np
import pandas as pd
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
        
        
    def get_twitter_client_api(self):
        return self.twitter_client

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



        
class TweetAnalyzer():
    
    def tweets_to_df(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['Tweet_length'] = np.array([len(tweet.text) for tweet in tweets])
        df['Number of Likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['Number of Retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['Date'] = np.array([tweet.created_at for tweet in tweets])   
        
           
           
        return df
        
if __name__ == "__main__":
    #pass
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    twan = TweetAnalyzer()
    #lis = TwitterStreamer().stream.tweets
    st = input("Enter username: ")
    num = int(input("Enter number of tweets: "))
    
    tweets = api.user_timeline(screen_name = st, count = num)
    #pd.set_option('display.max_colwidth', -1)
    df = twan.tweets_to_df(tweets)
    ch = 1
    
    while ch!=0:
        print("Press to get time series on:\n1. Tweet Length.\n2. Number of Likes.\n3.Number of Retweets.\n")
        print("0.Exit")
        ch = int(input("Enter your choice: "))
        
        if ch==1:
            st = "Tweet_length"
        elif ch==2:
            st = "Number of Likes"
        elif ch==3:
            st = "Number of Retweets"
        
        else:
            break
        
        time_likes = pd.Series(data = df[st].values, index = df['Date'])
        time_likes.plot(figsize = (16, 4), color = 'r')
        plt.show()
    
    ch = 1
    
    while ch!=0:
        print("Press to get information on:\n1. Tweet Length.\n2. Number of Likes.\n3.Number of Retweets.\n")
        print("4.ID.\n0.Exit")
        
        ch = int(input("Enter your choice: "))
        
        if ch==1:
            st = "Tweet_length"
        elif ch==2:
            st = "Number of Likes"
        elif ch==3:
            st = "Number of Retweets"
        elif ch==4:
            st = "id"

        else:
            break
        
        print(df[st])
        