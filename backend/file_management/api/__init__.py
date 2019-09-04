# coding=utf-8
import logging

from flask import Blueprint
from flask_restplus import Api

from file_management.extensions.exceptions import global_error_handler
from .register import ns as register_ns

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    app=api_bp,
    version='1.0',
    title='Register API',
    validate=False,
    # doc='' # disable Swagger UI
)


def init_app(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """
    api.add_namespace(register_ns)
    app.register_blueprint(api_bp)
    api.error_handlers[Exception] = global_error_handler
