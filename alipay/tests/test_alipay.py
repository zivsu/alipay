import config
from tests import BaseTestCase
from lib.alipay import AliWapPay

class BaseTestALiPay(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestALiPay, self).__init__(*args, **kwargs)
        self.alipay = AliWapPay(notify_url="http://27.42.109.37:8000",
                                app_id=config.ali_app_id,
                                private_key_path=config.private_key_path,
                                sign_type= config.ali_sign_type,
                                seller_id=config.ali_seller_id
                                )


class TestALiPay(BaseTestALiPay):
    def test_wappay_create_trade(self):
        trade_id = self.gen_uid()
        title = "test title"
        fee = "0.01"
        timeout = "1m"
        callback_url = "http://27.42.109.37:8000"
        product_info = {
            "title": "test title",
            "descr": "test descr",
            "type": "1"
        }
        query_string = self.alipay.create_trade(trade_id,
                                                fee,
                                                timeout,
                                                callback_url,
                                                product_info
                                                )
        self.assertIsNotNone(query_string)
        self.assertIn("sign", query_string)

    def test_refund(self):
        trade_id = self.gen_uid()
        fee = "0.01"
        query_string = self.alipay.refund(trade_id, fee)
        self.assertIsNotNone(query_string)
        self.assertIn("sign", query_string)