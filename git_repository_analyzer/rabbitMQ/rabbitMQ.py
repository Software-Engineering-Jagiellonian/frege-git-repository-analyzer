import sys
import json
import pika
import time

from git_repository_analyzer.analyzer.github_data_extractor import extract
from git_repository_analyzer.dbManager.db_manager import DbManager

dbM = DbManager()


def callback(ch, method, properties, body):
    #przeniesc to stad?
    time.sleep(body.count(b'.'))
    print(json.loads(body))
    repository = dbM.select_repository_by_id(json.loads(body)['repo_id'])
    print(repository)
    # extract('facebook', 'react')


class RabbitMQ:

    @staticmethod
    def connect(rabbitmq_host, rabbitmq_port, queue_name):
        while True:
            try:
                print(f'Connecting to RabbitMQ ({rabbitmq_host}:{rabbitmq_port})')
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
                channel = connection.channel()
                channel.confirm_delivery()
                channel.queue_declare(queue=queue_name, durable=True)

                print('Connected')
                return channel
            except pika.exceptions.AMQPConnectionError as exception:
                print(f'AMQP Connection Error: {exception}')
                print('Sleeping for 10 seconds and retrying')
                time.sleep(10)
            except KeyboardInterrupt:
                print('Exiting')
                try:
                    connection.close()
                except NameError:
                    pass
                sys.exit(0)

    @staticmethod
    def consume(channel, queue_name):
        while True:
            try:
                channel.basic_consume(on_message_callback=callback, queue=queue_name)
                channel.start_consuming()
                print("Message was consumed from RabbitMQ")
                break
            except pika.exceptions.NackError:
                print("That was problem with consume message from RabbitMQ, sleeping for 10 seconds")
                time.sleep(10)
