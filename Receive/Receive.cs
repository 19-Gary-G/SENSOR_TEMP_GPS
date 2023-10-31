using System;
using System.Text;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Threading;

namespace Receive
{
    class Program
    {
        static void Main(string[] args)
        {
            var factory = new ConnectionFactory() { HostName = "localhost" };

            using (var connection = factory.CreateConnection())
            {
                using (var channel = connection.CreateModel())
                {
                    channel.QueueDeclare(queue: "directions", durable: false, exclusive: false, autoDelete: false, arguments: null);

                    var consumer = new EventingBasicConsumer(channel);

                    consumer.Received += (model, ea) =>
                    {
                        var body = ea.Body.ToArray();
                        var message = Encoding.UTF8.GetString(body);

                        // Split the message into separate lines
                        var messages = message.Split(new[] { Environment.NewLine }, StringSplitOptions.None);

                        foreach (var msg in messages)
                        {
                            Console.WriteLine($"[X] Received {msg}");
                            // Introduce un retraso de 3 segundos entre cada mensaje
                            Thread.Sleep(100000);
                        }
                    };

                    channel.BasicConsume(queue: "directions", autoAck: true, consumer: consumer);

                    Console.WriteLine("Press any key to exit...");
                    Console.ReadLine();
                }
            }
        }
    }
}

