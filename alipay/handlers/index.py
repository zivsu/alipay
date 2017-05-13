import json

from tornado.web import HTTPError

from handlers import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")