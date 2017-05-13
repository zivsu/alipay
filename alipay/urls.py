#!/usr/bin/env python
# coding=utf-8

from handlers.index import IndexHandler
from handlers import wap


app = [
    (r"/", IndexHandler),
    (r"/trade/wap/pay", wap.WapPayHandler),
    (wap.URL_WAP_PAY_CALLBACK, wap.WapPayCallbackHandler),
    (wap.URL_WAP_PAY_NOTIFY, wap.WapPayNotifyHandler),
    (r"/trade/wap/refund", wap.WapRefundHandler),
]