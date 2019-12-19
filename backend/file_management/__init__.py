# coding=utf-8
import logging

import flask
import sentry_sdk
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration

from file_management.extensions.exceptions import NotFoundException, \
    UnAuthorizedException, BadRequestException, ForbiddenException
from file_management.extensions.sentry import before_send

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

SENTRY_DSN = 'SENTRY_DSN'


def create_app():
    import config
    import logging.config
    import os
    from flask_jwt_extended import JWTManager

    from . import api, models
    from file_management import helpers
    from file_management import services
    def load_app_config(app):
        """
        Load app's configurations
        :param flask.Flask app:
        :return:
        """
        app.config.from_object(config)
        app.config.from_pyfile('config.py', silent=True)

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(config.ROOT_DIR, 'instance')
    )
    load_app_config(app)

    # Register new flask project here and get new dsn: https://sentry.io
    dns = SENTRY_DSN if os.environ.get(
        'SEND_REPORT') == 'true' else None

    app.config['SENTRY_CONFIG'] = {
        'ignore_exceptions':    [NotFoundException, UnAuthorizedException,
                              BadRequestException, ForbiddenException],
        'level': logging.ERROR,
    }

    sentry_sdk.init(
        dsn=dns,
        integrations=[FlaskIntegration()],
        environment=app.config['ENV_MODE'],
        in_app_exclude=['app.extensions.exceptions'],
        before_send=before_send
    )

    # setup jwt extended
    app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # How long an access token should live before it expires. Set by minutes (int)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ['TOKEN_UPTIME']) * 60
    # app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    # app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
    # should not, but i will use it in this app.
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    jwt = JWTManager(app)

    app.config['CORS_SUPPORTS_CREDENTIALS'] = True

    # setup logging
    logging.config.fileConfig(app.config['LOGGING_CONFIG_FILE'],
                              disable_existing_loggers=False)

    app.secret_key = config.FLASK_APP_SECRET_KEY
    models.init_app(app)
    api.init_app(app)
    services.init_app(app)
    CORS(app)
    return app


app = create_app()
