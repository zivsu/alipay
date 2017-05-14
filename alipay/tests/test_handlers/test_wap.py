from urllib import quote_plus
import unittest
import mock

from tests import BaseHTTPTestCase
from lib.rsa import RSA, remove_spec
import config

class TestWapHandler(BaseHTTPTestCase):
    def new_trade(self):
        trade_id = self.gen_uid()
        fee = "1"
        query_params = {
            "trade_id": trade_id,
            "fee": fee,
            "show_url": "/",
            "timeout": "1",
            "title": "test title",
        }
        query_string = "&".join(["{}={}".format(k, quote_plus(v)) for k, v in query_params.items()])
        url = "/trade/wap/pay?{}".format(query_string)
        self.get(url)
        return trade_id, fee

    def test_pay(self):
        query_params = {
            "trade_id": self.gen_uid(),
            "fee": "1",
            "show_url": "http://localhost:4000",
            "timeout": "1",
            "title": "test title",
        }
        query_string = "&".join(["{}={}".format(k, quote_plus(v)) for k, v in query_params.items()])
        url = "/trade/wap/pay?{}".format(query_string)
        response = self.get(url)
        self.assertEqual(response.code, 200)

    def test_callback_403(self):
        url = "/trade/wap/pay/callback"
        response = self.get(url, callback=self.handle_json_response)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body["code"], 403)

    def test_callback(self):
        trade_id, fee = self.new_trade()

        query_params = {
            "app_id": config.ali_app_id,
            "auth_app_id": config.ali_app_id,
            "charset": "utf-8",
            "method": "alipay.trade.wap.pay.return",
            "out_trade_no": trade_id,
            "seller_id": config.ali_seller_id,
            "timestamp": "2017-04-03 02:00:09",
            "total_amount": fee,
            "trade_no": "2017040321001004890200292043",
            "version": "1.0"
        }

        items = sorted([(k, v) for k, v in query_params.items()])
        message = "&".join(["{}={}".format(k, v) for k,v in items])
        signature = RSA(config.private_key_path).sign(message)

        query_string = "&".join(["{}={}".format(k, quote_plus(v)) for k,v in items])
        url = "/trade/wap/pay/callback?" + query_string + "&sign={}".format(quote_plus(signature))

        signer = RSA(config.public_key_path).gen_signer()
        with mock.patch.object(RSA, "gen_signer", return_value=signer):
            response = self.get(url)
            self.assertEqual(response.code, 200)
            self.assertIn("html", response.body)

    def test_notify(self):
        trade_id, fee = self.new_trade()

        params = {
            "trade_no": trade_id,
            "out_trade_no": trade_id,
            "trade_status": "TRADE_SUCCESS",
            "total_amount": fee,
            "seller_id": config.ali_seller_id,
        }
        items = sorted([(k, v) for k, v in params.items()])
        message = "&".join(["{}={}".format(k, v) for k,v in items])
        signature = RSA(config.private_key_path).sign(message)

        body = "&".join(["{}={}".format(k, quote_plus(v)) for k,v in items])
        body = body + "&sign={}".format(quote_plus(signature))

        signer = RSA(config.public_key_path).gen_signer()
        with mock.patch.object(RSA, "gen_signer", return_value=signer):
            response = self.post("/trade/wap/pay/notify", body, force_dumps=False)
            self.assertEqual(response.code, 200)
            self.assertEqual(response.body, "success")