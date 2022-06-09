import os
from flasgger.utils import swag_from
from flask import request, Response, json, Blueprint

from helpers.decorators import expection_handler
from helpers.spelling import sql_semicolon_controller
from tdm.flask_app.all_services.sql_service.utils import get_oracle_sql_result, get_postgres_sql_result

sql_service = Blueprint('sql_service', __name__)


def __get_yml_file_path(yml_file_name):
    base_path = os.path.dirname(os.path.realpath('__file__'))
    package_name = __package__.split('.').pop()
    return os.path.abspath(os.path.join(base_path, './all_services', package_name, 'swagger_yml_files', yml_file_name))


@sql_service.route('/executeOracleSql', methods=['GET'])
@swag_from(__get_yml_file_path('execute_oracle_sql.yml'))
@expection_handler
def execute_sql():
    env = request.args.get('env', 'qa')
    camel_case_type = request.args.get('camelCase', 'false')
    sql = sql_semicolon_controller(request.args['sql'])

    return Response(json.dumps(get_oracle_sql_result(env, camel_case_type, sql)),
                    status=200,
                    mimetype='application/json'
                    )


@sql_service.route('/executePostgresSql', methods=['GET'])
@swag_from(__get_yml_file_path('execute_postgres_sql.yml'))
@expection_handler
def execute_postgres_sql():
    sql = sql_semicolon_controller(request.args['sql'])

    return Response(json.dumps(get_postgres_sql_result(sql)), status=200, mimetype='application/json')
