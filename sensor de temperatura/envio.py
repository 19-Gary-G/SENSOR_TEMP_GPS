import mysql.connector
import pika
import time

# Variable para rastrear el momento de la última consulta
ultimo_registro_id = 0

# Función para mostrar registros nuevos
def mostrar_registros_nuevos():
    global ultimo_registro_id
    # Establecer la conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="arduino",
        password="123456789",
        database="datos_sensor"
    )

    # Crear un cursor para interactuar con la base de datos
    cursor = conexion.cursor()

    # Consulta para seleccionar registros nuevos desde el último registro consultado
    consulta = "SELECT * FROM lecturas WHERE id > %s"
    cursor.execute(consulta, (ultimo_registro_id,))

    # Recuperar registros nuevos
    registros = cursor.fetchall()

    # Conexión a RabbitMQ
    conexion_rabbitmq = pika.BlockingConnection(pika.ConnectionParameters('192.168.137.86'))
    canal = conexion_rabbitmq.channel()
    canal.queue_declare(queue='directions')

    # Enviar registros nuevos a la cola RabbitMQ
    for registro in registros:
        id, humedad, temperatura, fecha_registro = registro
        mensaje = f"ID: {id}, Humedad: {humedad}, Temperatura: {temperatura}, Fecha: {fecha_registro}"
        canal.basic_publish(exchange='', routing_key='directions', body=mensaje)
        print(f"Mensaje enviado a la cola: {mensaje}")
        ultimo_registro_id = id

    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conexion.close()

    # Cerrar la conexión a RabbitMQ
    conexion_rabbitmq.close()

# Manejar la interrupción del usuario (Ctrl+C)
try:
    # Ciclo para mostrar registros nuevos y enviar a la cola RabbitMQ
    while True:
        mostrar_registros_nuevos()
        time.sleep(5)  # Consultar cada 5 segundos (ajusta el valor según tus necesidades)

        # Si no se encontraron registros nuevos en la última consulta, continúa
        if ultimo_registro_id == 0:
            continue

except KeyboardInterrupt:
    print("Programa detenido por el usuario")