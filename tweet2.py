import os
from dotenv import load_dotenv
import tweepy


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



# Create a tweet with media
media_path = "/Users/felipesilva/Downloads/circle-3041437_640.jpg"
media = api.media_upload(filename=media_path)
media_id = media.media_id
client.create_tweet(text="Automated twwet with media!", media_ids=[media_id])

# # Create a text tweet
# client.create_tweet(text="Automated tweet with media!")
#
# # delete tweet
# tweet_id = str(input("Enter tweet id: "))
# client.delete_tweet(id=tweet_id)
# print("✅ Tweet deleted")
