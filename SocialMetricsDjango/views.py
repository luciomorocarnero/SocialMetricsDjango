from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
from .API import *
import json
import datetime

# Create your views here.
def test(request):
    response = {}
    modelo = APITwitter('joerogan')
    # response = modelo.get()
    print(modelo.all())
    return JsonResponse(response, safe=False)