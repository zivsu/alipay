from models.logtrade import LogTrade, LogTradeMgr
from tests import BaseTestModelCase
import util

class TestLogTradeModel(BaseTestModelCase):
    def test_add(self):
        kwargs = {
            "component": "payment",
            "trade_id": self.gen_uid(),
            "payload": None,
            "inserted_at": util.utcnow()
        }
        log_trade = LogTrade(**kwargs)
        self.db.add(log_trade)
        self.db.commit()
        self.assertTrue(True)


class TestLogTradeMgr(BaseTestModelCase):
    def test_add(self):
        kwargs = {
            "trade_id": self.gen_uid(),
            "payload": {
                "field1": "value1",
                "field2": "value2"
            },
            "component": "payment"
        }
        LogTradeMgr.add(self.db, **kwargs)