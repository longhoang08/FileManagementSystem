# coding=utf-8
import logging

import pytest

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def app(request):
    from file_management import app
    from file_management.models import db, redis_client
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # test db initializations go below here
    db.create_all()
    redis_client.init_app(app)

    def teardown():
        db.session.remove()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)
    return app
