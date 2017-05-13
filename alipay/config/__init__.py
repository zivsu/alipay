import logging
from os import path

from tornado.options import options

_conf = '{}.config.py'.format(options.appname)
_conf = path.join(path.dirname(__file__), _conf)
execfile(_conf)
logging.info('loaded ' + _conf)

_conf = '{}.config.{}.py'.format(options.appname, options.env)
_conf = path.join(path.dirname(__file__), _conf)
if path.isfile(_conf):
    execfile(_conf)
    logging.info('loaded ' + _conf)