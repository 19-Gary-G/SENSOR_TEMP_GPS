import requests
import urllib
import time

api_url = "https://www.mapquestapi.com/directions/v2/route?"
key = "CKBK4LUutBLUZ47VhrcqU6TVSrJLaYuG"

def get_directions(origin, destination):
    url = api_url + urllib.parse.urlencode({"key": key, "from": origin, "to": destination})
    json_data = requests.get(url).json()
    status_code = json_data["info"]["statuscode"]

    if status_code == 0:
        trip_duration = json_data["route"]["formattedTime"]
        distance = json_data["route"]["distance"] * 1.61

        print("===================================================")
        print("")
        print(f"Recorrido de viaje desde {origin.capitalize()} hasta {destination.capitalize()}.")
        print(f"Tiempo de viaje: {trip_duration}")
        print("Distancia de recorrido: " + str("{:.2f}".format(distance) + " km"))
        print("")
        print("===================================================")
        print("")
        print("Seguimiento de recorrido")
        print("")

        # Almacenar las indicaciones en una lista
        directions = json_data["route"]["legs"][0]["maneuvers"]
        current_direction_index = 0  # Índice de la dirección actual

        while current_direction_index < len(directions):
            current_direction = directions[current_direction_index]
            direction_distance = current_direction["distance"] * 1.61
            print(current_direction["narrative"] + f" ({direction_distance:.2f} Km)")

            time.sleep(3)  # Esperar 3 segundos

            # Verificar si se ha alcanzado la distancia de esta indicación
            if distance <= direction_distance:
                current_direction_index += 1

            # Restar la distancia de la dirección actual a la distancia total
            distance -= direction_distance

        print("¡Has llegado a tu destino!")

while True:
    origin = input("Ubicacion origen: ")
    if origin == 'cerrar':
        break
    destination = input("Ubicacion destino: ")
    if destination == 'cerrar':
        break
    get_directions(origin, destination)
