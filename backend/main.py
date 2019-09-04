# coding=utf-8
import logging
import os

from dotenv import load_dotenv

from file_management import app

__author__ = 'Kien'
_logger = logging.getLogger(__name__)

_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

if __name__ == '__main__':
    app.run()
