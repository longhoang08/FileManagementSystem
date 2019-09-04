# coding=utf-8
import logging
import os

from dotenv import load_dotenv

_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

ROOT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__)
))
# The environment to run this config. This value will affect to the
# configuration loading
#
# it can be: dev, test, stag, prod
ENV_MODE = os.environ.get('ENV_MODE', '').upper()

DEBUG = True
TESTING = False
LOGGING_CONFIG_FILE = os.path.join(ROOT_DIR, 'etc', 'logging.ini')

FLASK_APP_SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['EMAIL_USER']
MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

REDIS_URL = "redis://:12345678@my_redis_service:6379/0"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
    MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, 3306, MYSQL_DATABASE
)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True


def _env(name, default):
    """ Get configuration from environment in priorities:
      1. the env var with prefix of $ENV_MODE
      2. the env var with the same name (in upper case)
      3. the default value

    :param str name: configuration name
    :param default: default value
    """

    def _bool(val):
        if not val:
            return False
        return val not in ('0', 'false', 'no')

    # make sure configuration name is upper case
    name = name.upper()

    # try to get value from env vars
    val = default
    for env_var in ('%s_%s' % (ENV_MODE, name), name):
        try:
            val = os.environ[env_var]
            break
        except KeyError:
            pass
    else:
        env_var = None

    # convert to the right types
    if isinstance(default, bool):
        val = _bool(val)
    return env_var, val


_IGNORED_CONFIG = (
    'ROOT_DIR',
    'STATIC_DIR',
    'ENV_MODE',
)

# rewrite all configuration with environment variables
_vars = list(locals().keys())
for name in _vars:
    if name in _IGNORED_CONFIG:
        continue
    if not name.startswith('_') and name.isupper():
        env_var, val = _env(name, locals()[name])
        locals()[name] = val
