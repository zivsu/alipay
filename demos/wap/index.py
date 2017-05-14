#!/usr/bin/env python
from __future__ import unicode_literals

import os
import logging
import uuid
from urllib import urlencode, quote_plus

from tornado.escape import json_decode, json_encode
from tornado.httpclient import HTTPError, HTTPClient, HTTPRequest
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/trade", TradeHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        )
        super(Application, self).__init__(handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class TradeHandler(tornado.web.RequestHandler):
    @property
    def host(self):
        return self.request.protocol + "://" + self.request.host

    def post(self):
        try:
            form = json_decode(self.request.body)
        except:
            raise HTTPError(400, "Could not decode JSON: {}".format(self.request.body))

        fee = form.get("fee", "")
        title = form.get("title", "")

        data = {
            "fee": fee,
            "title": title.encode("utf-8"),
            "trade_id": str(uuid.uuid4()).replace("-", ""),
            "timeout": 10,
            "show_url": self.host + "/trade",
        }
        query_params = urlencode(data)

        client = HTTPClient()
        request = HTTPRequest("http://localhost/trade/wap/pay?" + query_params)
        response = client.fetch(request)
        self.write({"url": response.body})

    def get(self):
        self.render("trade.html")


def main():
    tornado.options.parse_command_line()
    app = Application()
    logging.info("run on {} port".format(options.port))
    app.listen(options.port, xheaders=True)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()