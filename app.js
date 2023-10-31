const express = require('express');
const app = express();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const amqp = require('amqplib/callback_api');

// Configura el servidor HTTP y WebSocket
http.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});

// Conexión a RabbitMQ
amqp.connect('amqp://localhost', (error, connection) => {
  if (error) {
    throw error;
  }

  connection.createChannel((error, channel) => {
    if (error) {
      throw error;
    }

    const queue = 'directions';

    // Configura la cola RabbitMQ
    channel.assertQueue(queue, { durable: false });

    // Escucha mensajes de la cola y los envía a los clientes WebSocket
    channel.consume(
      queue,
      (message) => {
        const content = message.content.toString();
        io.sockets.emit('directions', content);
      },
      { noAck: true }
    );
  });
});

// Configura rutas de Express
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/logistica.html');
});

// Archivo HTML de ejemplo
app.get('/logistica.html', (req, res) => {
  res.sendFile(__dirname + '/logistica.html');
});

// Inicializa WebSocket para enviar mensajes en tiempo real
io.on('connection', (socket) => {
  console.log('A user connected');
});
