from flask import Flask, request
from flasgger import Swagger
from flasgger import LazyString, LazyJSONEncoder
from flask_caching import Cache

cache = Cache()

app = Flask(__name__)

app.config["SWAGGER"] = {
    "title": "Test Data Manager",
    "uiversion": 2,
    'description': 'Making easy to find test data!'
}

app.config['JSON_SORT_KEYS'] = False
app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DIR'] = '/tmp'

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder

swagger = Swagger(app, config=swagger_config, template=template)


def create_app():
    from tdm.flask_app.all_services.common_service.routes import common_service
    from tdm.flask_app.all_services.sql_service.routes import sql_service
    app.register_blueprint(common_service)
    app.register_blueprint(sql_service)

    cache.init_app(app)
    return app
