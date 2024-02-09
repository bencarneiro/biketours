from django.core.management.base import BaseCommand
import tweepy
import os
import instagrapi
from mastodon import Mastodon
import facebook
import requests
import pytumblr
from py3pin.Pinterest import Pinterest
# from linkedin import linkedin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        photo = graph.put_photo(image=upload.read(), album_path='me/photos', published=True, message=text)
    photo_id = photo['id']
    post_url = f"https://www.facebook.com/{page_id}/photos/{photo_id}"


def post_to_tumblr(text, filepath):
    tumblr_consumer_key = os.environ.get("TUMBLR_CONSUMER_KEY", "")
    tumblr_consumer_secret = os.environ.get("TUMBLR_CONSUMER_SECRET", "")
    tumblr_token = os.environ.get("TUMBLR_TOKEN", "")
    tumblr_token_secret = os.environ.get("TUMBLR_TOKEN_SECRET", "")

    client = pytumblr.TumblrRestClient(
        tumblr_consumer_key,
        tumblr_consumer_secret,
        tumblr_token,
        tumblr_token_secret
        )
    
    client.create_photo("hippiecity", state="published", tags=["austin", "austintx", "biketours", "tours", "austinevents", "austinmeetups", "austintours", "austinvacation", "austinparks"],
        caption=text,
        data=filepath)

# Make the request
    print(client.info())
    # client.info()


def post_to_pintereset(text, image_path):
    pinterest_username="biketours@bencarneiro.com"
    tumblr_pw = os.environ.get("PINTEREST_PASSWORD", "")

    driver = webdriver.Chrome()
    driver.implicitly_wait(15) # seconds
    driver.get("http://www.pinterest.com")
    # login = driver.find_element(By.LINK_TEXT, "Log in")
    login = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div/div/div[1]/div/div[2]/div[2]")
    login.click()
    email = driver.find_element(By.ID, "email")
    email.clear()
    email.send_keys(pinterest_username)
    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys(tumblr_pw)
    login = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[7]/button")
    login.click()
    page_is_loaded = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div/div/div[4]/div/a/div/div/span"))
    )
    driver.get("https://www.pinterest.com/hippie_city/bike/")
    post_pin = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[5]/div/div/div/div/div/div/button")
    post_pin.click()
    create_pin = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[5]/div/div[2]/div/div/div/div[1]/div[2]")
    create_pin.click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[1]/div/div[1]/div/input").send_keys(image_path)
    
    #title
    title = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div/span/div/input").send_keys("Austin Bike Tours")
    
    description = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/span"))
    ).send_keys(text)
    # description = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/div/span/span").send_keys(text)
    # description.click()
    link = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[3]/div/div/div[2]/div/div/div[3]/div/div[1]/div/span/div/input").send_keys("https://hippie.city")
    wait = WebDriverWait(driver, 10)
    for x in range(5):
        try:
            submit_pin = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]/div[2]/div/button"))
            ).click()
        except:
            print("error")

# def post_to_linkedin(tweet):


    # API_KEY = '86zkt4ad8b6szo'
    # API_SECRET = 'HBNtEZDckfdQ56Q4'
    # RETURN_URL = 'https://hippie.city'
    # ACCESS_TOKEN = os.environ.get("LINKEDIN_ACCESS_TOKEN_2", "")
    
    # headers = {
    #     "Content-Type": "application/json",
    #     "X-Restli-Protocol-Version": "2.0.0",
    #     "Authorization": "Bearer " + ACCESS_TOKEN
    # }
    # me = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    # print(me.json())
    # # Initialize the LinkedIn application
    # # app = linkedin.LinkedInApplication(token=ACCESS_TOKEN)

    # # Define the content you want to post
    # post_content = {"author": "urn:li:organization:101550409",
    #             "lifecycleState": "PUBLISHED",
    #             "specificContent": {
    #                 "com.linkedin.ugc.ShareContent": {
    #                     "shareCommentary": {
    #                         "text": "This is a test post from a command-line interface! #austin #bikes"
    #                     },
    #                     "shareMediaCategory": "NONE"
    #                 }
    #             },
    #             "visibility": {
    #                 "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    #             }
    #         }
    # image_url = "https://www.tumblr.com/hippiecity/741723619442475008/come-ride-bikes-and-experience-the-healing-magic"

    # # Post the content to your business page
    # # try:
    # #     app.submit_share(post_content, submitted_image_url=image_url, visibility={'code': 'anyone'})
    # #     print("Post successfully submitted to LinkedIn business page.")
    # # except Exception as e:
    # #     print("LINKEDIN EMERGENCY")
    # #     print(e)
    # post_url = "https://api.linkedin.com/v2/ugcPosts"
    # try:
    #     response = requests.post(post_url, headers=headers, json=post_content)
    #     if response.status_code == 201:
    #         print("Post successfully submitted to LinkedIn business page.")
    #     else:
    #         print("Error occurred while posting:", response.text)
    # except Exception as e:
    #     print("Error occurred:", e)

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
        # post_to_facebook(tweet_body, filepath_to_media)
        # post_to_tumblr(tweet_body, filepath_to_media)
        post_to_pintereset(tweet_body, filepath_to_media)
        # post_to_linkedin(tweet_body)