from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from . import models
from .API import *
import json
import datetime
from http import HTTPStatus

# Create your views here.
def test(request):
    response = {}
    model = APIYoutube().by_userName('@joerogan')
    print(model.id)
    return JsonResponse(response, safe=False)

def endpoints(request):
    endpoints = [
        {
            'url': 'api/twitter',
            'params': {
                'userName': "userName of the twitter profile like 'joerogan'",
                'history': "if exists return twitter profile history stats, unique for each day",
                'update': "force scrape and bypass cache"
            }
        }
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
    
    response = api.get(cache=False) if update else api.get()
    return JsonResponse(response, safe=False)
