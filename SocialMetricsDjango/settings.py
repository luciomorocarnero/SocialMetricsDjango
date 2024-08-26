from dotenv import load_dotenv
import os
import datetime

load_dotenv()

# KEYS
YOUTUBE_KEY = os.getenv('YOUTUBE_KEY')


# Twitter
class TwitterConfig:
    MAX_TWEETS: int = 20
    DEFAULT_IMG: str = r'https://nzbirdsonline.org.nz/sites/all/files/2X2A1697%20King%20Penguin%20bol.jpg'
    DEFAULT_VIDEO: str = r'No video found'
    MAX_TRIES: int = 3
    LOG_LEVEL: int = 1
    SKIP_INSTANCE_CHECK: bool = False
    CACHE_TIMEDELTA: datetime.timedelta = datetime.timedelta(days=7)