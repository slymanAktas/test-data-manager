from pathlib import Path

import psycopg2
from psycopg2 import pool

from db_operations.connection.db_functions import Connection


class PostgresDB:

    @property
    def database(self):
        return "app_tdmanager"

    @property
    def user(self):
        return "usr_tdmanager"

    @property
    def password(self):
        return 'tXC+9V8M' if self.__is_localhost else 'wE!#9M5K'

    @property
    def host(self):
        return 'dpdbpsql01d' if self.__is_localhost else 'dpdbpsin01p'

    @staticmethod
    def __pwd():
        return Path(__file__).parent.parent.parent.parent

    @property
    def __is_localhost(self):
        return str(PostgresDB.__pwd()).__contains__('/User')


postgres_db = PostgresDB()

try:
    connection_pool = pool.ThreadedConnectionPool(
        20,
        20,
        database=postgres_db.database,
        user=postgres_db.user,
        password=postgres_db.password,
        host=postgres_db.host
    )
except (Exception, psycopg2.DatabaseError) as error:
    raise Exception("Error while connecting to PostgreSQL", error)


class Postgres(Connection):
    __instance = None

    def connect(self):
        if self.__instance is None:
            self.__instance = connection_pool.getconn()
        return self.__instance

    def get_connection(self):
        return self.__instance

    def release_connection(self):
        # Release the connection to the pool
        connection_pool.putconn(self.connection)

        # Close the pool
        # connection_pool.closeall()

    def fetch_row(self, cursor, sql, which_row):
        cursor.execute(sql)
        return cursor.fetchone() if which_row == 'one' else cursor.fetchall()


def postgres(env=None):
    return Postgres(env)
