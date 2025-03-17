import tweepy
import random
import time
import os
import json

# Load Twitter API credentials from environment variables or a config file
# Replace these with your actual credentials
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Load occupations from the text file
with open('occupations.txt', 'r') as file:
    occupations = [line.strip() for line in file]

# Shuffle the list to ensure randomness
random.shuffle(occupations)

# Path to the file that keeps track of used occupations
used_occupations_file = 'used_occupations.json'

# Load used occupations from the file
if os.path.exists(used_occupations_file):
    with open(used_occupations_file, 'r') as file:
        used_occupations = json.load(file)
else:
    used_occupations = []

# Function to post a tweet
def post_tweet(occupation):
    tweet = f"A {occupation} could easily be a software dev, but a software dev could never be a {occupation}."
    api.update_status(tweet)
    print(f"Tweeted: {tweet}")

# Main loop
while True:
    for occupation in occupations:
        if occupation not in used_occupations:
            post_tweet(occupation)
            used_occupations.append(occupation)
            with open(used_occupations_file, 'w') as file:
                json.dump(used_occupations, file)
            # Wait for a random time interval between 1 and 24 hours
            time.sleep(random.randint(3600, 86400))
    
    # Reset used occupations once all have been used
    used_occupations = []
    with open(used_occupations_file, 'w') as file:
        json.dump(used_occupations, file)
    random.shuffle(occupations)
