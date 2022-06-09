from re import sub

from db_operations.connection.oracle.connect_to_oracle import oracle
from db_operations.connection.postgres.connect_to_postgres import postgres


def execute_select_operation(env, camel_case_type, sql):
    all_row = []
    for each_row in oracle(env).fetch_all(sql):
        one_row = {}
        for key, value in each_row.items():
            one_row[camelCase(key) if camel_case_type == "true" else key] = convert_value_to_propoer_format(value)
        all_row.append(one_row)
    return all_row


def convert_value_to_propoer_format(value):
    import cx_Oracle
    import json
    import datetime
    if isinstance(value, cx_Oracle.LOB):
        return json.loads(str(value))
    elif isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%dT%H:%M:%S')
    else:
        return value


def camelCase(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])


def get_oracle_sql_result(env, camel_case_type, sql):
    if str(sql).lower().startswith('select'):
        return execute_select_operation(env, camel_case_type, sql)
    else:
        oracle(env).update_via_sql(sql)
        return {'status': 'success'}


def get_postgres_sql_result(sql):
    if str(sql).lower().startswith('select'):
        return postgres().fetch_one(sql)
    else:
        try:
            postgres().postgres_sql_execute_and_commit(sql)
            return {'status': 'success'}
        except Exception as exc:
            raise {'Insertion was failed as': str(exc)}
