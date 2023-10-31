import requests
import urllib
import time
import pika

api_url = "https://www.mapquestapi.com/directions/v2/route?"
key = "CKBK4LUutBLUZ47VhrcqU6TVSrJLaYuG"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='directions')

def send_message_to_queue(message):
    channel.basic_publish(exchange='', routing_key='directions', body=message)

def get_directions(origin, destination):
    url = api_url + urllib.parse.urlencode({"key": key, "from": origin, "to": destination})
    json_data = requests.get(url).json()
    status_code = json_data["info"]["statuscode"]

    if status_code == 0:
        trip_duration = json_data["route"]["formattedTime"]
        distance = json_data["route"]["distance"] * 1.61

        directions = json_data["route"]["legs"][0]["maneuvers"]

        for current_direction in directions:
            direction_distance = current_direction["distance"] * 1.61
            direction_info = current_direction["narrative"] + f" ({direction_distance:.2f} Km)"
            send_message_to_queue(direction_info)
            time.sleep(10)

        send_message_to_queue("¡Has llegado a tu destino!")

while True:
    origin = input("Ubicación origen: ")
    if origin == 'cerrar':
        break
    destination = input("Ubicación destino: ")
    if destination == 'cerrar':
        break
    get_directions(origin, destination)

connection.close()
