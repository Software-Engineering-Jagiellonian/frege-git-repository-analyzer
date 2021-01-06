import logging
import sys
import pika
import time

from git_repository_analyzer.config import config


class RabbitMQ:

    def connect(self):
        logging.info('Connecting to the rabbitMQ instance...')
        self.params = config.config('rabbitMQ')
        while True:
            try:
                logging.info(f"Connecting to RabbitMQ {self.params['host']}: {self.params['port']}")
                # logging.info('Connecting to RabbitMQ', self.params['host'], ":", self.params['port'])
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.params['host'], port=self.params['port']))
                channel = connection.channel()
                channel.confirm_delivery()
                channel.queue_declare(queue=self.params['queue'], durable=True)

                logging.info('Connected')
                return channel
            except pika.exceptions.AMQPConnectionError as exception:
                logging.error(f'AMQP Connection Error: {exception}')
                logging.info('Sleeping for 10 seconds and retrying')
                time.sleep(10)
            except KeyboardInterrupt:
                logging.info('Exiting...')
                try:
                    connection.close()
                except NameError:
                    pass
                sys.exit(0)

    def consume(self, channel, callback):
        while True:
            try:
                channel.basic_consume(on_message_callback=callback, queue=self.params['queue'])
                channel.start_consuming()
                logging.info("Message was consumed from RabbitMQ")
                break
            except pika.exceptions.NackError:
                logging.error("That was problem with consume message from RabbitMQ, sleeping for 10 seconds")
                time.sleep(10)
