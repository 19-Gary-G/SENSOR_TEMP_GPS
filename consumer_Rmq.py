import pika

def callback(ch, method, properties, body):
    try:
        city = body.decode('utf-8')
        print(f"Received '{city}' from the queue")

        # Aquí puedes implementar la lógica para buscar el clima en base a la ciudad.
        # Por ejemplo, puedes hacer una solicitud HTTP a tu servicio de clima.

        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que se ha procesado el mensaje
    except Exception as e:
        print(f'Error processing message: {e}')
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que se ha procesado el mensaje incluso si hay un error

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queue_name = 'Clima_cigueña'
channel.queue_declare(queue=queue_name, durable=False)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

print('Waiting for messages. To exit, press Ctrl+C')

channel.start_consuming()
