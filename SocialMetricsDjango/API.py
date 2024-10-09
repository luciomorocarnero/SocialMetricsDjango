from .models import ServiceRequest
from .settings import *

import logging
import datetime
from http import HTTPStatus
import dateparser
from dataclasses import dataclass

from ntscraper import Nitter #Scrapper For twitter
import requests

logger = logging.getLogger(__name__)

class APIBase:
    """Base model for APIs managment, saves and search request"""
    
    def __init__(self, service: str) -> None:
        assert service in [ser[0] for ser in ServiceRequest.SERVICES], ValueError('No service support')
        self.service = service
    
    def _save(self, params: dict, data: dict):
        try:
            model = ServiceRequest(service=self.service, params=params, data=data)
            model.save()
            logger.info(f'APIBase - {self.service} - saving request:')
        except Exception as e:
            logger.error(f'APIBase - {self.service} - error saving request: {e}')

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
        """
        Search last request till the cache_time
        
        :param params: params for searching requests
        :param cache_time: timedelta object for search requests, can cahce in TwitterConfig in SocialMetricsDjango/setting.py
        
        :return: a response with status, cache_reponse: bool, cache_date, result
        """    
        last_request = self._last_request(params)
        if not last_request:
            logger.debug(f'APIBase - {self.service} - {params} - Cache - No last requests')
            return None
        
        date = datetime.datetime.now(datetime.timezone.utc) - cache_time
        if last_request.created_at < date:
            logger.debug(f'APIBase - - {self.service} - {params} - Cache - last_request.created_at < cache_date')
            return None
        
        response = {
            'status': HTTPStatus.OK,
            'cache_response': True,
            'cache_date': last_request.created_at.date().isoformat(),
            'result': last_request.data
        }
        
        return response

class RequestsHandler:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, endpoint: str, params: dict = None, headers: dict = None) -> dict:
        """
        Makes a GET request to the specified endpoint with optional query parameters and headers.
        
        The method automatically handles common exceptions like HTTP errors, timeouts, 
        and too many redirects, logging the appropriate error message if any issue arises.
        
        :param endpoint: The API endpoint to which the request will be made (e.g., "/data").
        :param params: Optional dictionary of query parameters to include in the request.
        :param headers: Optional dictionary of HTTP headers to include in the request.
        
        :return: A dictionary containing the JSON response from the server, or an empty dictionary 
                 if an error occurred or no valid response was received.
                 
        :raises: Requests exceptions such as HTTPError, Timeout, TooManyRedirects, etc., are caught
                 and logged, but not re-raised.
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f'RequestsHandler - Making GET request to "{url}" with params {params} and headers {headers}')
        
        params = params or {}
        headers = headers or {}

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            logger.info(f'Response from {url} received successfully. Status Code: {response.status_code}')
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error(f'HTTPError - URL: {url}, Status Code: {response.status_code}, Response: {response.text}')
        except requests.exceptions.Timeout as e:
            logger.error(f'Request to {url} timed out: {e}')
        except requests.exceptions.TooManyRedirects as e:
            logger.error(f'TooManyRedirects - URL: {url}, Error: {e}')
        except requests.exceptions.RequestException as e:
            logger.error(f'Request failed: {e}')

        return {}
        
    
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
            logger.error(f'APITwitter - Error fetching tweets - userName: "{self.username}" - {e}')
            return []
        
    def __get_profile_info(self, scraper) -> dict:
        try:
            return scraper.get_profile_info(self.username)
        except Exception as e:
            logger.error(f'APITwitter - Error fetching profile info userName: "{self.username}" - {e}')
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
                logger.info(f'{self.service} Data Cache Response Success for "{self.username}"')
                return response
        
        logger.info(f'APITwitter - Making Scrape for "{self.username}"')
        scraper = Nitter(log_level=TwitterConfig.LOG_LEVEL, skip_instance_check=TwitterConfig.SKIP_INSTANCE_CHECK)
        tweets = self.__get_tweets(scraper)
        profile = self.__get_profile_info(scraper)
        if not tweets or not profile:
            logger.error(f'APITwitter - Twitter Scraper no fetch for "{self.username}"')
            return {
                'status': HTTPStatus.INTERNAL_SERVER_ERROR,
                'error': "Twitter Scraper couldn't fetch data"    
                }
            
        logger.info(f'APITwitter - Twitter Data Fetch ok for "{self.username}"')           
        response = {
            'status': HTTPStatus.OK,
            'cache_response': False,
            'result': self.__clean(profile, tweets)
        }        
        self.save(response['result'])
        return response
        
    def __clean(self, profile, tweets) -> dict:
        """Clear fetched data and add statistics """
        logger.debug(f'APITwitter - Cleaning Data for "{self.username}"')
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
                'picture': tweet.get('pictures', [TwitterConfig.DEFAULT_IMG])[0] if tweet.get('pictures') else '',
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
            more_statistics = {key: round(value / total_tweets) for key, value in more_statistics.items()}
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
        """
        Return a list of requests
        
        :param unique: gives only a set of requests by days
        """
        data = super()._all().filter(params=self.params)
        if not unique:
            return data
        days = set([q.created_at.date() for q in data])
        return [data.filter(created_at__date=day).first() for day in days]
    
    def history(self):
        """Return a list of requests data for Twitter Profile like ...{date, data{'profile'}}"""
        data = self.all(unique=True)
        return [{'date':x.created_at.date().isoformat(), 'stats':x.data.get('profile', {}).get('stats')} for x in data]
    
class APIYoutube(APIBase):
    
    def __init__(self, id: str) -> None:
        super().__init__('Youtube')
        
        self.base_url = "https://www.googleapis.com/youtube/v3"
        if not YoutubeConfig.KEY:
            raise ValueError('Not youtube key loaded')
        self.api_key = YoutubeConfig.KEY
        
        self.id = id
        self.params = {
            'id': self.id
        }
    
    @classmethod
    def by_userName(cls, userName: str):
        """
        Retrieves the YouTube API object based on a given username.

        This method searches for an existing profile linked to the provided username. 
        If a matching profile is found, it returns an instance of the APIYoutube class 
        initialized with the relevant ID. If no profile is found, make a requests to
        youtube api

        :param userName: A string representing the username to search for.
                         
        :return: An instance of the APIYoutube class if a profile is found.
        """
        if not userName.startswith('@') or ' ' in userName:
            logger.error(f'APIYoutube - "{userName}" -The username must start with '@' and must not have spaces.')
            return None
        service_request = ServiceRequest.objects.filter(service='Youtube', data__profile__userName__iexact=userName).first()

        if service_request:
            youtube_id = service_request.data.get('profile', {}).get('id')
            logger.info(f'APIYoutube - Find id: "{youtube_id}" for userName: "{userName}"')
            return cls(id=youtube_id)
        else:
            logger.info(f'APIYoutube - No YouTube profile id found for username: "{userName}"')
            logger.info(f'APIYoutube - Making profile request for "{userName}"')
            ...
            

    # def 
    