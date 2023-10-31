const amqp = require('amqplib');
const fetch = require('node-fetch'); // Para hacer solicitudes HTTP

async function sendTemperature() {
  try {
    const connection = await amqp.connect('amqp://192.168.137.86');
    const channel = await connection.createChannel();
    const queue = 'directions';

    await channel.assertQueue(queue, { durable: false });

    const city = 'Cancun';

    // Función para enviar la temperatura y programar el próximo envío
    const sendAndScheduleNext = async () => {
      try {
        const weatherData = await fetch(`https://es.wttr.in/${city}?format=j1`);
        const weatherJson = await weatherData.json();
        const temperature = weatherJson.current_condition[0].temp_C;

        channel.sendToQueue(queue, Buffer.from(`La temperatura actual de ${city} es ${temperature}°C`));
        console.log(`Sent temperature of ${temperature}°C for ${city} to the queue`);

        // Programar el próximo envío después de 10 segundos
        setTimeout(sendAndScheduleNext, 10);
      } catch (error) {
        console.error('Error sending message:', error);
      }
    };

    // Iniciar el envío periódico
    sendAndScheduleNext();
  } catch (error) {
    console.error('Error sending message:', error);
  }
}

sendTemperature();




