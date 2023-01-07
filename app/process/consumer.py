import pika
import json
from .search import getNearestNeigbors,ClusterAndClassifyToDB
from .producer import publish

param=pika.URLParameters("amqps://pgmqkkhl:DC516D0tzh9OnHejzCbzyyh3VaJJUIxE@kangaroo.rmq.cloudamqp.com/pgmqkkhl")
connection=pika.BlockingConnection(param)
channel=connection.channel()
def callback(ch,method,properties,body):
    data=json.loads(body) 
    if(data== "-1"):
        #ClusterAndClassifyToDB()
        print(type(data))
    else:
        predection=getNearestNeigbors(data['latitude'],data['longitude'])[0]
        message=str(predection)
        #publish(message)
        
channel.basic_consume(queue="REQUEST_QUEUE",on_message_callback=callback,auto_ack=True)


print("Starting consumer")
channel.start_consuming()

    
    
    
    

        
