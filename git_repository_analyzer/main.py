import logging
import time 
import json

import sys
from pathlib import Path
root_path = Path(__file__).parent.parent
sys.path.insert(0, f'{root_path}')

from git_repository_analyzer.analyzer.github_data_extractor import extract_github_data
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
    print(json.loads(body))
    repository = dbM.select_repository_by_id(json.loads(body)['repo_id'])
    values = parse_url(repository['repo_url'])
    entry = extract_github_data(repository['repo_id'], values['owner'], values['repo_name'])
    dbM.save_repository_statistics(entry)


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