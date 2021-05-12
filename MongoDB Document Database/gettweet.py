# gettweet.py
"""Downloads tweets and stores them in MongoDB."""
import json
import tweepy

class GetTweet(tweepy.StreamListener):
    """Manages incoming Tweet stream."""

    def __init__(self, api, database, limit=10000):
        """Create instance variables for tracking number of tweets."""
        self.db = database
        self.tweet_count = 0
        self.TWEET_LIMIT = limit
        super().__init__(api)

    def on_connect(self):
        """Called when your connection attempt is successful, enabling 
        you to perform appropriate application tasks at that point."""
        print('Connection successful\n')

    def on_data(self, data):
        """Called when Twitter pushes a new tweet to you."""
        self.tweet_count += 1
        json_data = json.loads(data)
        self.db.tweets.insert_one(json_data)
        print(f'    Screen name: {json_data["user"]["name"]}') 
        print(f'     Created at: {json_data["created_at"]}')         
        print(f'Tweets received: {self.tweet_count}')
        return self.tweet_count != self.TWEET_LIMIT
    
    def on_error(self, status):
        print(f'Error: {status}')
        return True
