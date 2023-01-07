from rest_framework.decorators import api_view
from django.http import HttpRequest,HttpResponse
from .process import search
import json
from .process import producer,consumer

consumer
''' @api_view(['GET'])
def welcome(HttpRequest):
    #search.ClusterAndClassifyToDB()
    #predection=search.getNearestNeigbors(49.2221045,-0.4440154)
   # num=predection[0]
   # value=str(num)
    producer.publish('2')
    
    return HttpResponse("proccessing data please wait ...") 


@api_view(['POST'])
def getNearestAddress(HttpRequest):
    requestBody = HttpRequest.body.decode('utf-8')
    data=json.loads(requestBody) 
    predection=search.getNearestNeigbors(data['latitude'],data['longitude'])
    return HttpResponse(predection)
     '''
