import sqlite3
from sqlite3 import OperationalError, DatabaseError

from tdm.db_operations.connection.db_functions import Connection, DbUser


class Sqlite(Connection):
    def connect(self, env):
        return sqlite3.connect('test_data_manager.db', check_same_thread=False)

    def get_connection(self):
        pass

    def get_db_user(self, env) -> DbUser:
        pass

    def release_connection(self):
        pass

    def fetch_row(self, cursor, sql, which_row):
        try:
            cursor.execute(sql)
        except OperationalError as op_err:
            raise DatabaseError(f"{op_err}")
        return cursor.fetchone() if which_row == 'one' else cursor.fetchall()


def sqlite(env=None):
    return Sqlite(env)
