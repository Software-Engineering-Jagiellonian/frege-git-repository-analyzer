import psycopg2
from git_repository_analyzer.config import config


# todo import logger

def connect():
    params = config.config("credentials.ini")
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
    def save_repository_statistics(self, entry):
        cnn = self.connection
        cur = cnn.cursor()
        query = "INSERT INTO repository_statistics VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        cur.execute(query, (entry['forks'], entry['watchers'], entry['updated_at'], entry['created_at'], entry['open_issues'], entry['subscribers_count'], entry['closed_issues'], entry['pr_open'], entry['pr_closed']))

    @db_persist
    def select_repository_by_id(self, id):
        cnn = self.connection
        cur = cnn.cursor()
        query = "SELECT * FROM repositories WHERE repo_id=%s;"
        cur.execute(query, id)
        repository = cur.fetchone()
        if repository:
            return repository

# create table repository_statistics
# (
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
#
# alter table repository_statistics
#     owner to postgres;
