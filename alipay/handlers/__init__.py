#!/usr/bin/env python
# coding:utf-8

import traceback
import logging

from tornado.options import options
from tornado.web import RequestHandler, HTTPError

import config
from handlers.validation import ValidationMixin
from lib.rsa import RSA
from models import DBSession


class BaseHandler(RequestHandler, ValidationMixin):
    def prepare(self):
        self.db = DBSession()

    def on_finish(self):
        self.db.close()

    def get_current_user(self):
        pass

    @property
    def host(self):
        return self.request.protocol + "://" + self.request.host

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
            logging.info("request arguments:{}".format(self.request.arguments))
        except:
            raise HTTPError(400, "Problems parsing JSON")


class APIHandler(BaseHandler):
    def finish(self, chunk=None, notification=None):
        if chunk is None:
            chunk = {}

        if isinstance(chunk, dict):
            chunk["code"] = 200

            if notification:
                chunk["message"] = notification

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(APIHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages."""
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]

            if isinstance(e, HTTPError):
                pass
            else:
                e = HTTPError(500)

            chunk = {"code": e.status_code}
            if e.log_message is not None:
                chunk["message"] = e.log_message
            if e.reason is not None:
                chunk["reason"] = e.reason

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])

            # if config.debug:
            #     chunk["exception"] = exception

            # if status_code == 500 and not config.debug:
            #     self._send_error_email(exception)

            self.clear()
            # Always return 200 OK for API errors.
            self.set_status(200)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            # self.finish(chunk)
            super(APIHandler, self).finish(chunk)
        except Exception:
            logging.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)


def authenticated(function):
    def wrapper(*args, **kwargs):
        handler = args[0]
        arguments = handler.request.arguments
        # Remove `sign` and `sign_type`
        items = sorted([(k, v[0]) for k, v in arguments.items() if "sign" not in k])
        message = "&".join(["{}={}".format(k,v) for k,v in items])

        signature = handler.get_argument("sign", "")
        charset = handler.get_argument("charset", "utf-8")
        sign_type = handler.get_argument("sign_type", "RSA2")

        rsa = RSA(config.ali_public_key_path, sign_type=sign_type)
        verification = rsa.verify(message, signature, charset)
        if not verification:
            raise HTTPError(403, "Verify signature faild", reason="Invalid signature")
        function(*args, **kwargs)
    return wrapper


class APIPayHandler(APIHandler):
    @property
    def notify_host(self):
        env = options.env
        return config.PROXY_HOST if env == config.ENV_LOCAL else self.host