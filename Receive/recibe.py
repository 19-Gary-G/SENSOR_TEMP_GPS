import pika

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    print(f"[X] Received {message}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=False, exclusive=False, auto_delete=False, arguments=None)

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print("Press any key to salir...")
input()