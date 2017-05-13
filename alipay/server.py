#!/usr/bin/env python
import logging

from tornado import ioloop
from tornado.options import options

import define
options.parse_command_line()

from application import app
import config

app.listen(options.port, xheaders=True)
logging.info("== Starting {}:{} with {} config ==".format(options.appname, options.port, options.env))

if __name__ == '__main__':
    ioloop.IOLoop.instance().start()