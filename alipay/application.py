#!/usr/bin/env python
import os

from tornado import web

import urls
import config

# Make filepaths relative to settings.
path = lambda root, *args: os.path.join(root, *args)
ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = path(ROOT, 'static')
TEMPLATE_ROOT = path(ROOT, 'templates')

settings = {
    "template_path":TEMPLATE_ROOT,
    "static_path":STATIC_ROOT,
    "cookie_secret": config.cookie_secret,
    "xsrf_cookies": config.xsrf_cookies,
    "debug": config.debug,
    "autoreload": config.autoreload,
}

handlers = getattr(urls, config.urls)

app = web.Application(handlers, **settings)