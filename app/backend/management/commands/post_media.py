from django.core.management.base import BaseCommand
import tweepy
import os
import instagrapi
from mastodon import Mastodon
import facebook
import requests

def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

def tweet(tweet_text, media_filepath):
    api_key = os.environ.get("TWITTER_CONSUMER_KEY", "")
    api_secret = os.environ.get("TWITTER_CONSUMER_SECRET", "")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN","")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET","")
    client_v1 = get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret)
    client_v2 = get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret)
    # media_path = "/home/tonydeals/app/biketours/app/backend/static/good_skyline_ben.jpg"
    media_ids = []
    try:
        if media_filepath:
            media = client_v1.media_upload(filename=media_filepath)
            media_ids += [media.media_id]
    except Exception as e:
        print("Error uploading media to twitter")
        print(e)
    try:
        if len(media_ids) == 0:
            client_v2.create_tweet(text=tweet_text)
        else:
            client_v2.create_tweet(text=tweet_text, media_ids=media_ids)
    except Exception as e:
        print("couldn't send tweet")
        print(e)

    # except Exception as e:
    #     print("tweet failed")
    #     print(e)


def upload_to_instagram(image_path, caption):
    # Create a new Instagram client
    instagram_username = os.environ.get("INSTAGRAM_USERNAME")
    instagram_password = os.environ.get("INSTAGRAM_PASSWORD")
    client = instagrapi.Client()
    
    # Login to Instagram
    client.login(instagram_username, instagram_password)
    
    # Upload the image
    media = client.photo_upload(image_path, caption=caption)
    
    # Print the URL of the uploaded post
    print(f"insta post URL: https://instagram.com/p/{media.dict()['code']}")
    
    # Logout from Instagram
    client.logout()


def post_to_mastodon(text, image_path):

    # Mastodon instance URL and access token
    instance_url = "https://bencarneiro.com"
    mastodon_token = os.environ.get("MASTODON_TOKEN")

    # Initialize Mastodon with the instance URL and access token
    mastodon = Mastodon(
        access_token=mastodon_token,
        api_base_url=instance_url
    )

    # Post the image
    media = mastodon.media_post(image_path, description='alt')

    # Post the image with description to your Mastodon account
    mastodon.status_post(status=text, media_ids=[media['id']])


def post_to_facebook(text, image_path):

    # Your Facebook Page Access Token
    facebook_page_token = os.environ.get("FACEBOOK_PAGE_TOKEN", "")
    page_id="61555831386128"
    # Initialize the Graph API with your page access token
    graph = facebook.GraphAPI(access_token=facebook_page_token)
    with open(image_path, 'rb') as upload:
        photo = graph.put_photo(image=upload.read(), album_path='me/photos', published=False, message=text)
    photo_id = photo['id']
    post_url = f"https://www.facebook.com/{page_id}/photos/{photo_id}"

class Command(BaseCommand):

    help = 'Post media to all socials'


    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("text", nargs="+", type=str)

        # Named (optional) arguments
        parser.add_argument(
            "--m",
            help="add filepath to uploadable media",
        )


    def handle(self, *args, **kwargs):

        tweet_body = kwargs["text"][0]
        filepath_to_media = None
        if kwargs['m']:
            filepath_to_media = kwargs['m']
        # tweet(tweet_body, filepath_to_media)
        # if filepath_to_media:
        #     upload_to_instagram(filepath_to_media, tweet_body)
        # post_to_mastodon(tweet_body, filepath_to_media)
        post_to_facebook(tweet_body, filepath_to_media)