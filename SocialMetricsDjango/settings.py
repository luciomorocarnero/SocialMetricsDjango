from dotenv import load_dotenv
import os


load_dotenv()

# KEYS
YOUTUBE_KEY = os.getenv('YOUTUBE_KEY')


# Twitter
class TwitterConfig:
    MAX_TWEETS = 20
    DEFAULT_IMG = r'https://nzbirdsonline.org.nz/sites/all/files/2X2A1697%20King%20Penguin%20bol.jpg'
    MAX_TRIES = 3
    
