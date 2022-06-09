import cx_Oracle
from cx_Oracle import OperationalError

from db_operations.connection.db_functions import Connection
from db_operations.connection.oracle.credentials.user import *


def oracle(env):
    env = env.lower()
    if env not in ["qa", "st", "test"]:
        raise Exception(f'Please check your environment name. It written as {env}...')

    return Oracle(env)


def init_pool_for(env, min, max):
    return cx_Oracle.SessionPool(
        user=user_info[env].get("username"),
        password=user_info[env].get("password"),
        dsn=user_info[env].get("dsn"),
        min=min,
        max=max,
        increment=1,
        getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,  # bir bağlantı boşa çıkana kadar thread i beklet
        threaded=True,
        encoding="UTF-8"
    )


user_info = {
    "qa": {
        "username": QaUser.USERNAME,
        "password": QaUser.PASSWORD,
        "dsn": QaUser.DSN
    },
    "test": {
        "username": TestUser.USERNAME,
        "password": TestUser.PASSWORD,
        "dsn": TestUser.DSN
    },
    "st": {
        "username": StUser.USERNAME,
        "password": StUser.PASSWORD,
        "dsn": StUser.DSN
    }
}

connection_pools = {
    "qa": init_pool_for("qa", min=20, max=20),
    "test": init_pool_for("test", min=5, max=5),
    "st": init_pool_for("st", min=5, max=5)
}


class Oracle(Connection):
    __pool = None
    __conn = None

    def __init__(self, env):
        self.env = env
        super().__init__()

    def connect(self):
        if self.__conn is None:
            self.__pool = connection_pools[self.env]
            self.__conn = self.__pool.acquire()
        return self.__conn

    def get_connection(self):
        return self.__conn

    def release_connection(self):
        self.__pool.release(self.connection)

    @staticmethod
    def make_dict_factory(cursor):
        columnNames = [d[0] for d in cursor.description]

        def create_row(*args):
            return dict(zip(columnNames, args))

        return create_row

    def fetch_row(self, cursor, sql, which_row):
        try:
            cursor.execute(sql)
        except OperationalError as op_err:
            raise Exception(f"!!!!!!!!!!!!!!!!!!!{op_err}!!!!!!!!!!!!!!!!!!!")
        cursor.rowfactory = Oracle.make_dict_factory(cursor)

        return cursor.fetchone() if which_row == 'one' else cursor.fetchall()
