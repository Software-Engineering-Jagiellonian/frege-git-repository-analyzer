import logging
import psycopg2

from git_repository_analyzer.config import config


def connect():
    params = config.config('postgresql')
    engine = psycopg2.connect(**params)
    return engine


class DbManager:
    def db_persist(func):
        def persist(self, *args):
            try:
                self.connection = connect()
                logging.info("Success calling db func: " + func.__name__)
                rv = func(self, *args)
            except (Exception, psycopg2.DatabaseError) as error:
                logging.error("Error in transction Reverting all other operations of a transction ", error)
                self.connection.rollback()
                raise
            else:
                self.connection.commit()
                logging.info("Transaction completed successfully")
            finally:
                if self.connection is not None:
                    logging.info("PostgreSQL connection is closed")
                    self.connection.close()
            return rv

        return persist

    @db_persist
    def save_repository_statistics(self, entry):
        cnn = self.connection
        cur = cnn.cursor()
        query = "INSERT INTO repository_statistics VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(query, (entry['repo_id'], entry['forks'], entry['watchers'], entry['updated_at'], entry['created_at'], entry['open_issues'], entry['closed_issues'], entry['subscribers_count'], entry['pr_open'], entry['pr_closed']))

    @db_persist
    def select_repository_by_id(self, id):
        cnn = self.connection
        cur = cnn.cursor()
        query = "SELECT * FROM repositories WHERE repo_id='%s';"
        cur.execute(query % (id))
        repository = cur.fetchone()
        if repository:
            entry = dict()
            entry['repo_id'] = repository[0]
            entry['git_url'] = repository[1]
            entry['repo_url'] = repository[2]
            entry['crawl_time'] = repository[3]
            entry['download_time'] = repository[4]
            entry['commit_hash'] = repository[5]
            return entry

# create table repository_statistics
# (
#     repo_id           varchar,
#     forks             varchar,
#     watchers          varchar,
#     updated_at        varchar,
#     created_at        varchar,
#     open_issues_count varchar,
#     subscribers_count varchar,
#     closed_issues     varchar,
#     pr_closed         varchar,
#     pr_open           integer
# );

# alter table repository_statistics
#     owner to postgres;
