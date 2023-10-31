import serial
import mysql.connector
import math

# Parámetros de conexión a la base de datos
db_config = {
    "host": "localhost",
    "user": "arduino",
    "password": "123456789",
    "database": "datos_sensor"
}

# Función para establecer una conexión a la base de datos
def connect_to_database(config):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Error en la conexión a la base de datos: {err}")
        return None, None

def main():
    # Establecer la conexión a la base de datos
    connection, cursor = connect_to_database(db_config)
    
    if connection is None:
        return  # No se pudo conectar a la base de datos

    arduino = serial.Serial('COM5', 9600)

    try:
        while True:
            datos = arduino.readline().decode('utf-8')
            if datos.startswith('Humedad:') and 'Temperatura:' in datos:
                # Separar la cadena de datos para extraer la humedad y temperatura
                datos_split = datos.split()
                humedad = float(datos_split[1])
                temperatura = float(datos_split[3])
                print(f'Humedad: {humedad} %, Temperatura: {temperatura} °C')

                if not (math.isnan(humedad) or math.isnan(temperatura)):
                    # Insertar los datos en la base de datos MySQL
                    sql = "INSERT INTO lecturas (humedad, temperatura) VALUES (%s, %s)"
                    values = (humedad, temperatura)
                    cursor.execute(sql, values)
                    connection.commit()
                else:
                    # Insertar valores nulos en caso de error
                    sql = "INSERT INTO lecturas (humedad, temperatura) VALUES (NULL, NULL)"
                    cursor.execute(sql)
                    connection.commit()
                    print("Valores nulos insertados en la base de datos debido a un error en la lectura.")
            elif "Error obteniendo los datos del sensor DHT11" in datos:
                # En caso de que se detecte el mensaje de error, insertar valores nulos
                sql = "INSERT INTO lecturas (humedad, temperatura) VALUES (NULL, NULL)"
                cursor.execute(sql)
                connection.commit()
                print("Valores nulos insertados en la base de datos debido a un error en la lectura.")
    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
    finally:
        arduino.close()
        connection.close()

if __name__ == "__main__":
    main()