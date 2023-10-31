import os
import urllib
import requests

from dotenv import load_dotenv
import tweepy
import sqlite3

import schedule
import time

def tweeter_authentication():
    # load env variables
    print("✅ Load env variables")
    load_dotenv()

    # Twitter API credentials
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET_KEY")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")

    client_id = os.getenv("CLIENT_ID")

    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret,
        access_token, access_token_secret
    )
    api = tweepy.API(auth)

    print("✅ Authenticated")

    return client, api


def create_media_tweet(api=tweeter_authentication()[1], client=tweeter_authentication()[0], media_path=None, text=None):
    # Create a tweet with media
    if media_path is None:
        media_path = input("Enter media path: ")

    if text is None:
        text = input("Enter tweet text: ")

    media_path = media_path
    media = api.media_upload(filename=media_path)
    media_id = media.media_id
    client.create_tweet(text=text, media_ids=[media_id])


def create_text_tweet(client=tweeter_authentication()[0], text=None):
    # Create a text tweet
    if text is None:
        text = input("Enter tweet text: ")

    client.create_tweet(text="Automated tweet with media!")


def delete_tweet(client=tweeter_authentication()[0], tweet_id=None):
    # delete tweet
    if tweet_id is None:
        tweet_id = str(input("Enter tweet id: "))

    client.delete_tweet(id=tweet_id)
    print("✅ Tweet deleted")


# choose a random tweet from the database
def choose_random_tweet():
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tweets WHERE posted = 0 ORDER BY RANDOM() LIMIT 1")
    random_tweet = c.fetchone()
    conn.close()

    return random_tweet


def job():
    client, api = tweeter_authentication()
    tweet = choose_random_tweet()

    img_url = tweet[5]
    print(img_url)
    response = requests.get(img_url)
    if response.status_code:
        fp = open(f'{tweet[1]}.png', 'wb')
        fp.write(response.content)
        fp.close()

    tweet_to_post = f'{tweet[2]} | {tweet[3]} | {tweet[4]}'

    # create_media_tweet
    create_media_tweet(api=api, client=client, media_path=f"{tweet[1]}.png", text=tweet_to_post)
    print("✅ Tweet created and posted")

    # set tweet as posted in the database
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()
    c.execute("UPDATE tweets SET posted = 1, posted_at_tweet = strftime('%Y-%m-%d %H-%M-%S','now') WHERE id = ?",
              (tweet[0],))
    conn.commit()
    conn.close()
    print("✅ Tweet set as posted in the database")

    # delete image
    os.remove(f'{tweet[1]}.png')
    print("✅ Image deleted")


if __name__ == "__main__":

    job()

