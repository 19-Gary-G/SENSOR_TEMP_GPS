const amqp = require('amqplib');

async function receive() {
  try {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    const queue = 'Clima_cigueña';

    await channel.assertQueue(queue, { durable: false });

    console.log('Waiting for messages...');

    channel.consume(queue, async (message) => {
      try {
        const city = message.content.toString();
        console.log(`Received '${city}' from the queue`);

        // Aquí puedes implementar la lógica para buscar el clima en base a la ciudad.
        // Puedes llamar a tu función fetchWeather desde aquí.

        channel.ack(message); // Confirma que se ha procesado el mensaje.
      } catch (error) {
        console.error('Error processing message:', error);
        channel.ack(message); // Confirma que se ha procesado el mensaje incluso si hay un error.
      }
    });
  } catch (error) {
    console.error('Error connecting to RabbitMQ:', error);
  }
}

receive();
