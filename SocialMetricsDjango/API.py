from .models import ServiceRequest
from .settings import *

import logging
import datetime
from http import HTTPStatus
from ntscraper import Nitter #Scrapper For twitter
import dateparser

logger = logging.getLogger(__name__)


class APIBase:
    
    def __init__(self, service: str) -> None:
        assert service in [ser[0] for ser in ServiceRequest.SERVICES], ValueError('No service support')
        self.service = service
    
    def _save(self, params: dict, data: dict):
        try:
            model = ServiceRequest(service=self.service, params=params, data=data)
            model.save()
        except Exception as e:
            logger.error(f'Twitter error saving request: {e}')

    def _all(self):
        return ServiceRequest.objects.filter(service=self.service)
    
    def _last_request(
        self, params: dict, 
        date_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        ):
        return ServiceRequest._last_request(service=self.service,params=params,date_time=date_time)
    
    def _cache(
        self,
        params: dict, 
        cache_time: datetime.timedelta = TwitterConfig.CACHE_TIMEDELTA
        ):
        
        last_request = self._last_request(params)
        if not last_request:
            return None
        
        date = datetime.datetime.now(datetime.timezone.utc) - cache_time
        if last_request.created_at < date:
            return None
        
        response = {
            'status': HTTPStatus.OK,
            'cache_response': True,
            'cache_date': last_request.created_at.date().isoformat(),
            'result': last_request.data
        }
        
        logging.info(f'{self.service} Data Cache Response')           
        return response
    
    
class APITwitter(APIBase):
    
    def __init__(self, username: str) -> None:
        super().__init__('Twitter')
        self.username = username
        self.params = {
            'userName': self.username
        }
        
    def __get_tweets(self, scraper) -> list:
        try:
            return scraper.get_tweets(self.username, mode='user', number=TwitterConfig.MAX_TWEETS).get('tweets', [])
        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            return []
        
    def __get_profile_info(self, scraper) -> dict:
        try:
            return scraper.get_profile_info(self.username)
        except Exception as e:
            logger.error(f"Error fetching profile info: {e}")
            return {}
        
    def get(self, cache: bool = True) -> dict:
        """
        Get profile data and tweets based on the username and store it in the database.
        
        This method fetches the profile and tweets of the specified username using 
        the Nitter scraper. It then cleans the data and returns a dictionary with 
        the status of the request and the processed data.
        
        :param cache: bool, indicate if cache is active
        
        :return: dict
            A dictionary containing the following keys:
            - 'status' (HTTPStatus): The HTTP status of the response indicating success or failure.
            - 'cache_response' (bool): Indicates whether the response is cached or not.
            - 'date': date from the response
            - 'profile' (dict): A dictionary containing the user's profile information.
            - 'tweets' (list): A list of dictionaries where each dictionary represents a tweet.
        """
        if cache:
            response = self._cache(self.params)
            if response:
                return response
        
        scraper = Nitter(log_level=TwitterConfig.LOG_LEVEL, skip_instance_check=TwitterConfig.SKIP_INSTANCE_CHECK)
        tweets = self.__get_tweets(scraper)
        profile = self.__get_profile_info(scraper)
        if not tweets or not profile:
            logging.error('Twitter Scraper no fetch')
            return {
                'status': HTTPStatus.BAD_REQUEST,
                'error': "Twitter Scraper couldn't fetch data"    
                }
            
        logging.info('Twitter Data Fetch ok')           
        response = {
            'status': HTTPStatus.OK,
            'cache_response': False,
            'result': self.__clean(profile, tweets)
        }        
        self.save(response['result'])
        return response
        
    def __clean(self, profile, tweets) -> dict:
        """Clear fetched data and add statistics """
        
        tweets = [tweet for tweet in tweets if self.username in tweet.get('link', '')]
        data = {
            'profile': {},
            'tweets': []
        }
        more_statistics = {'avgRetweets':0, 'avgLikes':0,'avgComments':0, 'avgQuotes':0}

        for tweet in tweets:
            stats = tweet.get('stats', {})
            d = {
                'user': tweet.get('user', {}),
                'url': tweet.get('link','#'),
                'text': tweet.get('text', ''),
                'picture': tweet.get('pictures', [TwitterConfig.DEFAULT_IMG])[0] if tweet.get('pictures') else TwitterConfig.DEFAULT_IMG,
                'video': tweet.get('videos', [TwitterConfig.DEFAULT_VIDEO]),
                'statistics': stats,
                'datetime': dateparser.parse(tweet.get('date', '26/06/2003 15:00')).isoformat()
            }
            data['tweets'].append(d)

            more_statistics['avgRetweets'] += int(stats.get('retweets', 0))   
            more_statistics['avgLikes'] += int(stats.get('likes', 0))   
            more_statistics['avgComments'] += int(stats.get('comments', 0))   
            more_statistics['avgQuotes'] += int(stats.get('quotes', 0))   

        total_tweets = len(tweets)
        if total_tweets > 0:
            more_statistics = {key: str(round(value / total_tweets)) for key, value in more_statistics.items()}
        else:
            more_statistics = {key: 0 for key, value in more_statistics.items()}
        data['profile'] = profile
        data['profile']['joined'] = dateparser.parse(profile.get('joined','26/06/2003 15:00')).isoformat()
        data['profile']['stats'].update(more_statistics)
        
        return data
    
    def save(self, data: dict) -> None:
        """Save the response to the db"""
        self._save(params=self.params, data=data)
        
    def last_request(self, date_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)):
        """
        Search last response after selected date of the object
        
        :params datetime: must be in utc like 'datetime.datetime(tzinfo=datetime.timezone.utc)'
        :return: None if not match and object if it's found
        """
        return self._last_request(self.params, date_time)
    
    def all(self, unique = False):
        data = super()._all().filter(params=self.params)
        if not unique:
            return data
        days = set([q.created_at.date() for q in data])
        return [data.filter(created_at__date=day).first() for day in days]
