#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime
import json
import logging
from urllib import quote_plus

from lib.rsa import RSA

__all__ = ["AliWebPay", "AliWapPay"]


class BaseAliPay(object):
    def __init__(self, app_id=None, notify_url=None, private_key_path=None,
                 seller_id=None, sign_type=None, charset="utf-8"):
        self._app_id = app_id
        self._notify_url = notify_url
        self._seller_id = seller_id
        self._sign_type = sign_type
        self._charset = charset
        self._private_key_path = private_key_path

    def create_trade(self, data):
        return self._build_url_query_string(data)

    def refund(self, data):
        return self._build_url_query_string(data)

    def _build_url_query_string(self, data):
        signed_message = self._sign(data)
        quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in data.iteritems())

        return quoted_string + "&sign=" + quote_plus(signed_message)

    def _sign(self, data):
        """Sign message with private key."""
        unsigned_items = self._ordered_data(data)
        unsigned_message = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

        return RSA(self._private_key_path).sign(unsigned_message, self._charset)

    def _ordered_data(self, data):
        return sorted([(k, v) for k, v in data.iteritems()])


class AliWebPay(BaseAliPay):
    serveice = "create_direct_pay_by_user"

    def create_trade(self, out_trade_no, subject, fee, return_url):
        """Create trade pay order

        Args:
            out_trade_no (str): Unique order number.
            subject (str): Product title / order title / order keyword and so on.
            fee (int): The total amount of order, Currency unit is yuan.
            return_url (str): Start with `HTTP / HTTPS`
        Returns:
            A url of create trade order and pay.
        """
        data = {
            "service": self.service,
            "partner": self._seller_id,
            "_input_charset": self._charset,
            "notify_url": self._notify_url,
            "return_url": return_url,
            "out_trade_no": out_trade_no,
            "subject": subject,
            "payment_type": "1",
            "total_fee": str(fee),
            "seller_id": self._seller_id
        }
        # Web pay type do not add `sign_type` to sign
        return super(AliWebPay, self).create_trade(data) + "&sign_type=" + self._sign_type


class AliWapPay(BaseAliPay):
    version = "1.0"

    def create_trade(self, trade_id, fee, timeout, callback_url, product_info):
        """Create trade pay order

        Args:
            trade_id (str): Unique order number.
            fee (int): The total amount of order, Currency unit is yuan.
            timeout (string): The order allows the latest payment time,
                overdue will close the transaction. Value range: 1m - 15d
            callback_url (str): Start with `HTTP / HTTPS`.
            product_info (:obj:`dict`): product info of the trade.
        Returns:
            A url of create trade order and pay.
        """
        biz_content = {
            "out_trade_no": trade_id,
            "total_amount": str(fee),
            "timeout_express": timeout,
            "product_code": "QUICK_MSECURITY_PAY",
            "subject": product_info["title"],
            "body": product_info["descr"],
            "goods_type": product_info["type"],
        }
        biz_content_str = json.dumps(biz_content, separators=(',', ':'))

        data = {
            "app_id": self._app_id,
            "method": "alipay.trade.wap.pay",
            "charset": self._charset,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": self.version,
            "sign_type": self._sign_type,
            "notify_url": self._notify_url,
            "return_url": callback_url,
            "biz_content": biz_content_str
        }
        logging.info("wap trade data:{}".format(data))
        return super(AliWapPay, self).create_trade(data)

    def refund(self, trade_id, fee):
        biz_content = {
            "out_trade_no": trade_id,
            "refund_amount": str(fee),
        }
        biz_content_str = json.dumps(biz_content, separators=(',', ':'))

        data = {
            "app_id": self._app_id,
            "method": "alipay.trade.refund",
            "format": "JSON",
            "charset": self._charset,
            "sign_type": self._sign_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": self.version,
            "biz_content": biz_content_str
        }
        logging.info("wap refund data:{}".format(data))
        return super(AliWapPay, self).refund(data)