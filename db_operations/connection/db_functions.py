import time
from abc import ABC, abstractmethod
from cx_Oracle import DatabaseError
import psycopg2


class Connection(ABC):
    def __init__(self):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def fetch_row(self, cursor, sql, row):
        pass

    @abstractmethod
    def release_connection(self):
        pass

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def get_cursor(self):
        return self.cursor

    def execute_sql(self, sql):
        query_result = self.get_cursor().execute(sql)
        self.release_connection()
        return query_result

    def postgres_sql_execute_and_commit(self, sql):
        self.get_cursor().execute(sql)
        self.get_connection().commit()
        self.release_connection()

    def update(self, table_name, attribute, visitor):
        self.get_cursor().execute(
            f'UPDATE {table_name} SET {attribute[0]} = {attribute[1]} WHERE {visitor[0]} = {(visitor[1])}'
        )
        self.get_connection().commit()
        self.release_connection()

    def update_via_sql(self, sql):
        self.get_cursor().execute(sql)
        self.get_connection().commit()
        time.sleep(1 / 4)
        self.release_connection()

    def insert(self, table_name, attributes):
        try:
            self.get_cursor().execute(f"INSERT INTO {table_name} VALUES {attributes}")
        except psycopg2.errors.UniqueViolation:
            self.get_cursor().execute('ROLLBACK')
            self.delete_row(table_name, attributes)
            self.insert(table_name, attributes)
        self.get_connection().commit()
        time.sleep(1 / 4)
        self.release_connection()

    def insert_via_sql(self, sql):
        self.get_cursor().execute(sql)
        self.get_connection().commit()
        time.sleep(1 / 4)
        self.release_connection()

    def delete_row(self, table_name, attributes):
        self.get_cursor().execute(f"DELETE FROM {table_name} WHERE ID = '{attributes[0]}'")
        self.get_connection().commit()
        self.release_connection()

    def drop_table(self, table_name):
        self.get_cursor().execute(f'DROP TABLE {table_name}')
        self.get_connection().commit()
        self.release_connection()

    def fetch_one(self, sql):
        result = self.fetch_row(self.get_cursor(), sql, 'one')
        self.release_connection()
        return self.check_sql_results(result, sql)

    def fetch_all(self, sql):
        result = self.fetch_row(self.get_cursor(), sql, 'all')
        self.release_connection()
        return self.check_sql_results(result, sql)

    @staticmethod
    def check_sql_results(result, sql):
        if result is None or result.__len__() == 0:
            raise DatabaseError(f'Please check your sql. It returns empty! -->> {sql}')
        else:
            return result

    def create_table(self, table_name, **kwargs):
        attributes = ''
        for key, value in kwargs.items():
            attributes += f'{key} {value},'
        self.update_via_sql(f'''
            CREATE TABLE IF NOT EXISTS
            {table_name}(
            {attributes[:-1]}
            );
            ''')

    def create_sequence(self, sequeance_name):
        self.get_cursor().execute(f'CREATE SEQUENCE IF NOT EXISTS {sequeance_name}')
        self.get_connection().commit()
        self.release_connection()
