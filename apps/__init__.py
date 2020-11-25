import os

from flask import Flask
from flasgger import Swagger
from bases.globals import db, settings
from bases.converter import RegexConverter


def register_extensions(app):
    db.init_app(app)
    Swagger(app)
    return app


def register_converter(app):
    app.url_map.converters['re'] = RegexConverter
    return app


def register_router(app):
    from routers.v1 import routers as v1_routers
    for _r in v1_routers:
        app.register_blueprint(_r)
    return app


def register_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(pathname)s %(lineno)s %(module)s.%(funcName)s %(message)s',
    )

    if not os.path.exists(app.config['LOG_PATH']):
        os.makedirs(app.config['LOG_PATH'])

    if not os.path.exists(app.config['TEMP_PATH']):
        os.makedirs(app.config['TEMP_PATH'])

    file_handler_info = RotatingFileHandler(
        filename='{}/{}'.format(
            app.config['LOG_PATH'],
            app.config['LOG_PATH_FILE'],
        ),
        maxBytes=app.config['LOG_FILE_MAX_BYTES'],
        backupCount=app.config['LOG_FILE_BACKUP_COUNT']
    )
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(logging.INFO)
    app.logger.addHandler(file_handler_info)


def create_app():
    """
    :return: app
    """
    app = Flask(__name__.split('.')[0])
    app.config = settings
    register_extensions(app)
    register_converter(app)
    register_logging(app)
    register_router(app)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)



