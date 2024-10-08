from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from . import models
from .API import *
import json
import datetime
from http import HTTPStatus
from .settings import YoutubeConfig
# Create your views here.
def test(request):
    response = {}
    # modelo = APITwitter('joerogan')
    # a = modelo.all(unique=False)
    # print(a.first().data)
    return JsonResponse(response, safe=False)

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
