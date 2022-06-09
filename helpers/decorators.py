import sqlite3
import cx_Oracle
import json
import logging
import time
from functools import wraps
from flask import Response
from jenkinsapi.custom_exceptions import UnknownJob, NotInQueue, JenkinsAPIException
from werkzeug.exceptions import BadRequestKeyError

from helpers.exceptions import MockException, RunPathExeption


def logger(func):
    '''
    Log yazmasını istediğimiz method'un üzerine
    '@logger' decorator'u yazılır.
    İşleme ait log'lar all_services paketi altında '$METHOD_NAME.log' file'ı altına yazılır.

    @logger
    def method_name():
    '''

    logging.basicConfig(filename='{}.log'.format(func.__name__), level=logging.INFO)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(
            '"{}" ran with args: {} and kwargs: {}'.format(func.__name__, args, kwargs)
        )
        return func(*args, **kwargs)

    return wrapper


def timer(func):
    '''
    Execute edilmesi ne kadar sürdüğünü bilmek istediğimiz method'un üzerine
    '@timer' decorator'u yazılır.

    @timer
    def method_name():
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        exec = func(*args, **kwargs)
        t2 = round(time.perf_counter() - t1, 2)
        print('Takes {} seconds to execute "{}()".'.format(t2, func.__name__))
        return exec

    return wrapper


def expection_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            exec = func(*args, **kwargs)
            return exec

        except cx_Oracle.DatabaseError as error:
            if str(error).__contains__('-->>'):
                msj, sql = str(error).split(' -->> ')
                table_name = str(sql).split()[5].split('=')[0]
                data = {'message': msj,
                        'sql': str(sql).strip(),
                        'solution-recomandation': f'{table_name} should not be present in selected environment db'
                        }
                return Response(json.dumps(data), status=404, mimetype='application/json')
            else:
                data = {
                    'message': str(error),
                    'solution-recomandation': 'Please check your parameters. It shouldn\'t be defined on this environment!'
                }
                return Response(json.dumps(data), status=404, mimetype='application/json')

        except sqlite3.DatabaseError as error:
            data = {'message': str(error)}
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except FileNotFoundError as error:
            data = {'message': str(error)}
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except BadRequestKeyError as error:
            data = {
                'message': str(error),
                'solution-recomandation': f'Check your request parameters ({error.args}) inside routers.py'
            }
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except UnknownJob as job_name:
            data = {'message': f'Please check job name.It written as {job_name}!'}
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except KeyError as error:
            data = {
                'message': str(error),
                'solution-recomandation': 'Authentication failed. Please check your login credential!'
            }
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except NotInQueue:
            data = {'message': 'Job is not in queue!'}
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except JenkinsAPIException:
            data = {'message': 'Job will be deleted from queue ASAP!'}
            return Response(json.dumps(data), status=404, mimetype='application/json')

        except AttributeError as att:
            raise Exception(att)

        except MockException as mock_exception:
            data = {'message': mock_exception.message}
            return Response(json.dumps(data), status=200, mimetype='application/json')

        except RunPathExeption as path_excepiton:
            data = {'message': path_excepiton.message}

            return Response(json.dumps(data), status=200, mimetype='application/json')

        except ConnectionError as connection_error:
            data = {
                'message': str(connection_error),
                'solution-recomandation': 'Please check your urls!'
            }
            return Response(json.dumps(data), status=200, mimetype='application/json')

        # Exception must be bottom of the method
        except Exception as general_exception:
            data = {'message': str(general_exception)}
            return Response(json.dumps(data), status=404, mimetype='application/json')

    return wrapper
