from django.shortcuts import render
from django.http import HttpResponse
from . import models
import json
import datetime

# Create your views here.
def test(request):
    # Convierte el diccionario a una cadena JSON
    params_json = json.dumps({'nombre': 'lucio'})
    data_json = json.dumps({'nombre': 'lucio'})
    
    # Crea una instancia del modelo con los datos JSON
    modelo = models.ServiceRequest(
        params=params_json,  # Usa la cadena JSON en lugar de dict
        data=data_json,      # Usa la cadena JSON en lugar de dict
        service='Twitter'
    )
    
    # Guarda el modelo en la base de datos
    # modelo.save()
    bool = models.ServiceRequest.exist_request(params=params_json,service='Twitter')
    print(bool)
    return HttpResponse("Modelo guardado exitosamente")