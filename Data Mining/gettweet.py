# gettweet.py
"""Processes tweets from stream as they arrive."""
from textblob import TextBlob
import tweepy

class GetTweet(tweepy.StreamListener):
    """Manages incoming Tweet stream."""

    def __init__(self, api, limit=10):
        """Create instance variables for tracking number of tweets."""
        self.tweet_count = 0
        self.TWEET_LIMIT = limit
        super().__init__(api)

    def on_connect(self):
        """Called when your connection attempt is successful, enabling 
        you to perform appropriate application tasks at that point."""
        print('Connection successful\n')

    def on_status(self, status):
        """Called when Twitter pushes a new tweet to you."""
        try:  
            text = status.extended_tweet.full_text
        except: 
            text = status.text
        print(f'Screen name: {status.user.screen_name}:')
        print(f'   Language: {status.lang}')
        print(f'     Status: {text}')
        if status.lang != 'en':
            print(f' Translated: {TextBlob(text).translate()}')
        print()
        self.tweet_count += 1 
        return self.tweet_count <= self.TWEET_LIMIT
