import requests
import urllib

api_url = "https://www.mapquestapi.com/directions/v2/route?"
key = "CKBK4LUutBLUZ47VhrcqU6TVSrJLaYuG"

while True:
    origin = input("Ubicacion origen: ")
    if origin == 'cerrar':
        break
    destination = input("Ubicacion destino: ")
    if destination == 'cerrar':
        break
    url = api_url + urllib.parse.urlencode({"key":key, "from":origin, "to":destination})
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
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distance_remaining = distance - each["distance"] * 1.61            
            print(each["narrative"] + " (" + str("{:.2f}".format(distance_remaining)) + " Km faltantes)")
            distance = distance_remaining
