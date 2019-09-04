# coding=utf-8
import os

from dotenv import load_dotenv

from config import _DOT_ENV_PATH

load_dotenv(_DOT_ENV_PATH)


def get_environ(environ_var):
    return os.environ[environ_var]
