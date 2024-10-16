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
    response = {}
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
                'userName': "Return id of userName if this is found",
                'history': "return youtube profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        },
        {
            'url': 'api/instagram',
            'params': {
                'userName': "Return id of userName if this is found",
                'history': "return youtube profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        }
    ]
    return JsonResponse(endpoints, safe=False)

async def api_twitter(request):
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
        response = await api.get(cache=False)
    else:
        response = await api.get(cache=True)
    
    return JsonResponse(response, safe=False)

async def api_youtube(request):
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
        response = await api.get(cache=False)
    else:
        response = await api.get(cache=True)
    
    return JsonResponse(response, safe=False)

async def api_instagram(request):
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
        response = await api.get(cache=False)
    else:
        response = await api.get(cache=True)
    
    return JsonResponse(response, safe=False)
