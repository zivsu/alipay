import os
import json

import mock
import unittest
from tornado.web import RequestHandler
from tornado.testing import AsyncHTTPTestCase

from application import app
from models import DBSession
from models.trade import Trade
from models.payment import Payment
from models.product import Product
from models.logtrade import LogTrade
from tests import helper


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def gen_uid(self):
        return helper.gen_uid()


class BaseTestModelCase(BaseTestCase):
    def setUp(self):
        self.db = DBSession()

    def tearDown(self):
        clear_db()


class BaseHTTPTestCase(AsyncHTTPTestCase):
    def tearDown(self):
        clear_db()

    def gen_uid(self):
        return helper.gen_uid()

    def get_app(self):
        return app

    @mock.patch.object(RequestHandler, "check_xsrf_cookie", mock.MagicMock(return_value=None))
    def post(self, url, body, force_dumps=True, callback=None, **kwargs):
        if force_dumps:
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        kwargs.update({"body": body, "method": "POST"})
        if callback is None:
            return self.fetch(url, **kwargs)
        else:
            return callback(self.fetch(url, **kwargs))

    def get(self, url, callback=None, **kwargs):
        kwargs.update({"method": "GET"})
        if callback is None:
            return self.fetch(url, **kwargs)
        else:
            return callback(self.fetch(url, **kwargs))

    def handle_json_response(self, response):
        if response.error:
            return response
        else:
            response._body = json.loads(response.body)
            return response


def clear_db():
    """On teardown, remove all the db stuff"""
    db = DBSession()
    db.query(Payment).delete()
    db.query(Trade).delete()
    db.query(Product).delete()
    db.query(LogTrade).delete()
    db.commit()