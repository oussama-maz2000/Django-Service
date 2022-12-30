from rest_framework.decorators import api_view
from django.http import HttpRequest,HttpResponse
from .process import search
import json


@api_view(['GET'])
def welcome(HttpRequest):
    search.ClusterAndClassifyToDB()
    return HttpResponse("proccessing data please wait ...") 


@api_view(['POST'])
def getNearestAddress(HttpRequest):
    requestBody = HttpRequest.body.decode('utf-8')
    data=json.loads(requestBody) 
    predection=search.getNearestNeigbors(data['latitude'],data['longitude'])
    return HttpResponse(predection)
    
    