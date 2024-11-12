from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from . import models
from .API import *
import json
import datetime
from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)

def test(request):
    response = {
        'status': HTTPStatus.OK,
        'message': 'this is a test view, the server is running'
    }

    return JsonResponse(response, safe=False)

# TODO: Complete Enpoints
def endpoints(request):
    endpoints = [
        {
            'url': 'api/twitter',
            'params': {
                'userName': "userName of the twitter profile like 'joerogan'",
                'history': "return twitter profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        },
        {
            'url': 'api/youtube',
            'params': {
                'userName': "Requests by youtube profile username",
                'id': "Request by youtube profile id",
                'history': "return youtube profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        },
        {
            'url': 'api/instagram',
            'params': {
                'userName': "search param for instagram",
                'history': "return instagram profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        },
                {
            'url': 'api/tiktok',
            'params': {
                'userName': "search params, must have '@'",
                'history': "return tiktok profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        },
    ]
    return JsonResponse(endpoints, safe=False)

def api_twitter(request):
    userName = request.GET.get('userName')
    history = request.GET.get('history')
    update = request.GET.get('update')
    if not userName:
        response =  {
            'status': HTTPStatus.BAD_REQUEST,
            'error': 'Must provide a userName'
        }
        return JsonResponse(response, safe=False)
    
    api = APITwitter(userName)
    
    if history:
        response = {
            'status': HTTPStatus.OK,
            'user': api.username,
            'result': api.history()
        }
        return JsonResponse(response, safe=False)
    
    if update:
        logger.info('api_twitter - Forcing update')
        response = api.get(cache=False)
    else:
        response = api.get(cache=True)
    
    return JsonResponse(response, safe=False)

def api_youtube(request):
    id = request.GET.get('id')
    userName = request.GET.get('userName')
    history = request.GET.get('history')
    update = request.GET.get('update')
    if not ((userName and not id) or (not userName and id)):
        response =  {
            'status': HTTPStatus.BAD_REQUEST,
            'error': 'Must provide a userName or id'
        }
        return JsonResponse(response, safe=False)
    
    if userName:
        api = APIYoutube.by_userName(userName, api_key=YoutubeConfig.KEY)
    else:
        api = APIYoutube(id, api_key=YoutubeConfig.KEY)
    
    if history:
        response = {
            'status': HTTPStatus.OK,
            'id': api.id,
            'result': api.history()
        }
        return JsonResponse(response, safe=False)
    
    if update:
        logger.info('api_youtube - Forcing update')
        response = api.get(cache=False)
    else:
        response = api.get(cache=True)
    
    return JsonResponse(response, safe=False)

def api_instagram(request):
    userName = request.GET.get('userName')
    history = request.GET.get('history')
    update = request.GET.get('update')
    if not userName:
        response =  {
            'status': HTTPStatus.BAD_REQUEST,
            'error': 'Must provide a userName'
        }
        return JsonResponse(response, safe=False)
    
    api = APIIntagram(userName)
    
    if history:
        response = {
            'status': HTTPStatus.OK,
            'user': api.userName,
            'result': api.history()
        }
        return JsonResponse(response, safe=False)
    
    if update:
        logger.info('api_instagram - Forcing update')
        response = api.get(cache=False)
    else:
        response = api.get(cache=True)
    
    return JsonResponse(response, safe=False)


def api_tiktok(request):
    userName = request.GET.get('userName')
    history = request.GET.get('history')
    update = request.GET.get('update')
    if not userName:
        response =  {
            'status': HTTPStatus.BAD_REQUEST,
            'error': 'Must provide a userName'
        }
        return JsonResponse(response, safe=False)
    
    api = APITiktok(userName)
    
    if history:
        response = {
            'status': HTTPStatus.OK,
            'user': api.userName,
            'result': api.history()
        }
        return JsonResponse(response, safe=False)
    
    if update:
        logger.info('api_tiktok - Forcing update')
        response = api.get(cache=False)
    else:
        response = api.get(cache=True)
    
    return JsonResponse(response, safe=False)


def youtube(request):
    return render(request, 'SocialMetricsDjango/youtube.html')

def tiktok(request):
    return render(request, 'SocialMetricsDjango/tiktok.html')

def instagram(request):
    return render(request, 'SocialMetricsDjango/instagram.html')


def twitter(request):
    return render(request, 'SocialMetricsDjango/twitter.html')
