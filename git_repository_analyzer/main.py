import sys

from git_repository_analyzer.rabbitMQ import rabbitMQ

rabbit = rabbitMQ.RabbitMQ()



def run(rabbitmq_host, rabbitmq_port, queue_name):
    channel = rabbit.connect(rabbitmq_host, rabbitmq_port, queue_name)
    while True:
        rabbit.consume(channel, queue_name)


if __name__ == '__main__':
    try:
        rabbitmq_host = 'localhost'
    except KeyError:
        print("RabbitMQ host must be provided as RABBITMQ_HOST environment var!")
        sys.exit(1)

    try:
        rabbitmq_port = '5672'
    except ValueError:
        print("RABBITMQ_PORT must be an integer")
        sys.exit(2)

    try:
        queue = 'test'
    except KeyError:
        print("Destination queue must be provided as QUEUE environment var!")
        sys.exit(3)

    run(rabbitmq_host, rabbitmq_port, queue)
