# SENSOR_TEMP_GPS
SENSORES DE TEMPERATURA Y LOCALIZACION
El sistema de control de temperatura y localizaciòn que se lleva acabo por medio de:
- Sensor de temperatura interno en la cabina de la unidad conectado  a un base de datos en PhpMyAdmin.
- API de temperatura que nos brinda la información de la temepratura en la localización.
- API de localización que nos brinda la información desde el punto de partida hasta el de destino.
/Api_Temp Tiene los datos de temperatura exterior.
/sensor de temperatura Contiene los programas que se usan para la conexión de base de datos y temperatura interna.
/GPS_MAPS Continene el front y el programa de gps con localizacion.
/Receive Tiene el worker para poder llamar a las API con la queue de Rabbitmq "directions" 
