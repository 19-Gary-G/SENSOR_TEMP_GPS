import requests
import urllib
import pika
import json

api_url = "https://www.mapquestapi.com/directions/v2/route?"
key = "CKBK4LUutBLUZ47VhrcqU6TVSrJLaYuG"

# Establece la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

while True:
    origin = input("Ubicación origen: ")
    if origin == 'cerrar':
        break
    destination = input("Ubicación destino: ")
    if destination == 'cerrar':
        break
    url = api_url + urllib.parse.urlencode({"key": key, "from": origin, "to": destination})
    json_data = requests.get(url).json()
    status_code = json_data["info"]["statuscode"]

    if status_code == 0:
        trip_duration = json_data["route"]["formattedTime"]
        distance = json_data["route"]["distance"] * 1.61

        # Construye un diccionario con la información que deseas enviar a RabbitMQ
        message_data = {
            "origin": origin,
            "destination": destination,
            "trip_duration": trip_duration,
            "distance": distance
        }

        # Convierte el diccionario a JSON
        message_json = json.dumps(message_data)

        # Publica el mensaje en la cola de RabbitMQ
        channel.basic_publish(exchange='', routing_key='hello', body=message_json)

        print("Información enviada a RabbitMQ:")
        print(message_data)

# Cierra la conexión de RabbitMQ
connection.close()