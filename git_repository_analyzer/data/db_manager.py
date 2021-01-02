import psycopg2
from config.config import config
from datetime import datetime

# todo import logger

def connect():
    params = config("credentials.ini")
    engine = psycopg2.connect(**params)
    return engine


class DbManager:
    def db_persist(func):
        def persist(self, *args):
            try:
                self.connection = connect()
                print("success calling db func: " + func.__name__)
                rv = func(self, *args)
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error in transction Reverting all other operations of a transction ", error)
                self.connection.rollback()
                raise
            else:
                self.connection.commit()
                print("Transaction completed successfully")
            finally:
                if self.connection is not None:
                    print("PostgreSQL connection is closed")
                    self.connection.close()
            return rv

        return persist

    @db_persist
    def save_repository(self, repo_id, git_url, repo_url, download_time=None, commit_hash=None):
        cnn = self.connection
        cur = cnn.cursor()
        timestamp = datetime.now().astimezone().isoformat()
        query = "INSERT INTO repositories (repo_id, git_url, repo_url, crawl_time, download_time, commit_hash) VALUES (%s, %s, %s, %s, %s, %s);"
        cur.execute(query, (repo_id, git_url, repo_url, timestamp, download_time, commit_hash))
