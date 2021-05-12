# utilities.py
"""Utility functions for interacting with Tweepy objects."""
from geopy import OpenMapQuest
from textblob import TextBlob
import tweepy
import time 
import mykeys

def get_API(wait=True, notify=True):
    """Authenticate with Twitter and return API object."""
    auth = tweepy.OAuthHandler(mykeys.consumer_key, mykeys.consumer_secret)
    auth.set_access_token(mykeys.access_token, mykeys.access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=wait, 
                      wait_on_rate_limit_notify=notify)

def print_tweets(tweets):
    """For each Tweepy Status object in tweets, display the 
    user's screen name and tweet text. If the language is not
    English, translate the text with TextBlob."""
    for tweet in tweets:
        print(f'{tweet.user.screen_name}:', end=' ')
        if 'en' in tweet.lang:
            print(f'{tweet.text}\n')
        elif 'und' not in tweet.lang:
            print(f'\n  ORIGINAL: {tweet.text}')
            print(f'TRANSLATED: {TextBlob(tweet.text).translate()}\n')

def get_tweet_content(tweet, location=False):
    """Return dictionary with data from tweet (a Status object)."""
    data = {}
    data['screen_name'] = tweet.user.screen_name
    try:  
        data['text'] = tweet.extended_tweet.full_text
    except: 
        data['text'] = tweet.text
    if location:
        data['location'] = tweet.user.location
    return data

def get_geocodes(tweet_list):
    """Get the latitude and longitude for each tweet's location.
    Returns the number of tweets with invalid location data."""
    print('Getting tweet locations...')
    geo = OpenMapQuest(api_key=mykeys.mapquest_key)
    invalid = 0
    for tweet in tweet_list:
        processed = False
        delay = .1
        while not processed:
            try:
                geo_location = geo.geocode(tweet['location'])
                processed = True
            except:
                print('OpenMapQuest service timed out, trying again...')
                time.sleep(delay)
                delay += .1
        if geo_location:  
            tweet['latitude'] = geo_location.latitude
            tweet['longitude'] = geo_location.longitude
        else:  
            invalid += 1  # tweet['location'] was invalid
    print('Geocoding successful')
    return invalid
