from git_repository_analyzer.rabbitMQ import rabbitMQ

rabbit = rabbitMQ.RabbitMQ()

if __name__ == '__main__':
    while True:
        channel = rabbit.connect()
        rabbit.consume(channel)
