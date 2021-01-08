import logging
import time 
import json
import pika

import sys
from pathlib import Path
root_path = Path(__file__).parent.parent
sys.path.insert(0, f'{root_path}')

from git_repository_analyzer.analyzer.github_data_extractor import extract_github_data, extract_gitlab_data
from git_repository_analyzer.db.db_manager import DbManager
from git_repository_analyzer.rabbitMQ import rabbitMQ

rabbit = rabbitMQ.RabbitMQ()
dbM = DbManager()

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

# Callback is closure func passed to the rabbitMQ consume
def callback(ch, method, properties, body):
    time.sleep(body.count(b'.'))
    # print(json.loads(body))
    repo_primary_key = json.loads(body)['repo_id']
    repository = dbM.select_repository_by_id(repo_primary_key)
    values = parse_url(repository['repo_url'])
    repo_type = repo_primary_key.split('-')[0]

    if str(repo_type).lower() == 'github':
        entry = extract_github_data(repo_primary_key, values['owner'], values['repo_name'])
        dbM.save_repository_statistics(entry)
        ch.basic_ack(delivery_tag = method.delivery_tag)
    elif str(repo_type).lower() == 'gitlab':
        entry = extract_gitlab_data(repo_primary_key.split('-')[1])
        dbM.save_repository_statistics(entry)
        ch.basic_ack(delivery_tag = method.delivery_tag)
    else:
        # TODO: raise error
        logging.error(f'Invalid repository ID: {repo_primary_key}')


def parse_url(url: str):
    values = url.split('/')
    
    if len(values) < 4:
        #TODO: Raise error
        logging.error('Invalid url')
        return

    result = dict()
    result['owner'] = values[values.__len__()-2]
    result['repo_name'] = values[values.__len__()-1]
    return result


if __name__ == '__main__':
    setup_logger()
    logging.info('Starting application...')
    while True:
        channel = rabbit.connect()
        rabbit.consume(channel, callback)