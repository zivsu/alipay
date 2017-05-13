from enum import ChannelType, TradeStatus, ProductType
from models.trade import Trade, TradeMgr
from models.product import Product
from tests import BaseTestModelCase
import util

class TestTradeModel(BaseTestModelCase):
    def test_add(self):
        product = Product()
        product.title = "title"
        product.descr = "desc"
        product.type = ProductType.MATERIAL
        product.updated_at = product.inserted_at = util.utcnow()
        self.db.add(product)

        trade = Trade()
        trade.trade_id = self.gen_uid()
        trade.timeout = "1d"
        trade.fee = 0.01
        trade.status = TradeStatus.PENDING
        trade.channel = ChannelType.WAP
        trade.show_url = "url"
        trade.updated_at = trade.inserted_at = util.utcnow()
        trade.product = product

        self.db.add(trade)
        self.db.commit()
        self.assertTrue(True)


class TestTradeMgr(BaseTestModelCase):
    def test_is_unique(self):
        trade_id = self.gen_uid()
        is_unique = TradeMgr.is_unique(self.db, trade_id)
        self.assertTrue(is_unique)