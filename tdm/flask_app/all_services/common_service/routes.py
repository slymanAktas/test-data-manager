import os
from flasgger.utils import swag_from
from flask import Blueprint, Response, json

from helpers.decorators import expection_handler
from tdm.flask_app.all_services import cache
from tdm.flask_app.all_services.common_service.utils import generate_tckn

common_service = Blueprint('common_service', __name__)


def __get_yml_file_path(yml_file_name):
    base_path = os.path.dirname(os.path.realpath('__file__'))
    package_name = __package__.split('.').pop()
    return os.path.abspath(os.path.join(base_path, './all_services', package_name, 'swagger_yml_files', yml_file_name))


@common_service.route('/generateTckn', methods=['GET'])
@swag_from(__get_yml_file_path('generate_tckn.yml'))
@expection_handler
@cache.cached(timeout=5)
def get_tckn():
    return Response(json.dumps(generate_tckn()),
                    status=200, mimetype='application/json')
