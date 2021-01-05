import sys
import json
import pika
import time

from git_repository_analyzer.analyzer.github_data_extracter import extract
from git_repository_analyzer.dbManager.db_manager import DbManager
from git_repository_analyzer.config import config

dbM = DbManager()


def callback(ch, method, properties, body):
    # todo przeniesc to stad?
    time.sleep(body.count(b'.'))
    print(json.loads(body))
    repository = dbM.select_repository_by_id(json.loads(body)['repo_id'])
    # todo tu ma byc parser
    values = repository['repo_url'].split('/')
    extract(repository['repo_id'], values[0], values[1])

class RabbitMQ:

    def connect(self):
        self.params = config.config('rabbitMQ')
        while True:
            try:
                print('Connecting to RabbitMQ', self.params['host'], ":", self.params['port'])
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.params['host'], port=self.params['port']))
                channel = connection.channel()
                channel.confirm_delivery()
                channel.queue_declare(queue=self.params['queue'], durable=True)

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

    def consume(self, channel):
        while True:
            try:
                channel.basic_consume(on_message_callback=callback, queue=self.params['queue'])
                channel.start_consuming()
                print("Message was consumed from RabbitMQ")
                break
            except pika.exceptions.NackError:
                print("That was problem with consume message from RabbitMQ, sleeping for 10 seconds")
                time.sleep(10)
