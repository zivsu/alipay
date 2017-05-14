#!/usr/bin/env python
# coding=utf-8
import logging
import json

from tornado.web import HTTPError
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from sqlalchemy import update

import config
from enum import TradeStatus, ChannelType, ProductType
from handlers import authenticated, APIPayHandler, BaseHandler
from handlers.validation import RangeValidator
from lib.alipay import AliWapPay, RSA
from models.trade import Trade, TradeMgr
from models.product import Product
from models.payment import Payment
from models.logtrade import LogTradeMgr
import util


URL_WAP_PAY_CALLBACK = "/trade/wap/pay/callback"
URL_WAP_PAY_NOTIFY = "/trade/wap/pay/notify"

class WapPayHandler(APIPayHandler):
    def get(self):
        trade_id = self.valid("trade_id")
        title = self.valid("title")
        fee = self.valid("fee", force_type=float,
                         validator=RangeValidator(0.01, 100000000).validate)
        show_url = self.valid("show_url")
        # Minutes as the calculating unit.
        timeout = self.valid("timeout", force_type=int)

        # Optional arguments
        descr = self.valid("descr", required=False)
        type_ = self.valid("type", required=False) or ProductType.MATERIAL

        if self.errors:
            reason=self.errors.values()[0]
            raise HTTPError(422, "Validation Failed", reason=reason)

        # Validate `trade_id` unique.
        is_unique = TradeMgr.is_unique(self.db, trade_id)
        logging.info("trade id:{} is_unique:{}".format(trade_id, is_unique))
        if not is_unique:
          reason = "Trade ID is not unique"
          raise HTTPError(422, "Validation Failed", reason=reason)

        timeout = "{}m".format(str(timeout))
        title = title.encode("utf-8")

        notify_url = self.notify_host + URL_WAP_PAY_NOTIFY
        alipay = AliWapPay(notify_url=notify_url,
                           app_id=config.ali_app_id,
                           private_key_path=config.private_key_path,
                           sign_type= config.ali_sign_type,
                           seller_id=config.ali_seller_id
                           )

        # Create trade URL query string.
        product_info = {"title": title, "type": type_, "descr": descr}
        callback_url = self.host + URL_WAP_PAY_CALLBACK
        trade_qs = alipay.create_trade(trade_id,
                                       fee,
                                       timeout,
                                       callback_url,
                                       product_info
                                       )

        utcnow = util.utcnow()
        product = Product(title=title,
                          descr=descr,
                          type=type_,
                          updated_at=utcnow,
                          inserted_at=utcnow
                          )
        trade = Trade(trade_id=trade_id,
                      fee=fee,
                      status=TradeStatus.PENDING,
                      channel=ChannelType.WAP,
                      show_url=show_url,
                      inserted_at=utcnow,
                      updated_at=utcnow,
                      timeout=timeout,
                      product=product
                      )

        self.db.add_all([product, trade])
        self.db.commit()
        self.write(config.ali_gateway + "?" + trade_qs)


class WapPayCallbackHandler(APIPayHandler):
    @authenticated
    def get(self):
        logging.info("request arguments:{}".format(self.request.arguments))
        total_amount = self.get_argument("total_amount", None)
        timestamp = self.get_argument("timestamp", None)
        trade_id = self.valid("out_trade_no", None)

        # Add log.
        kwargs = {
          "trade_id": trade_id,
          "component": "wap_callback",
          "payload": self.request.arguments
        }
        LogTradeMgr.add(self.db, **kwargs)

        trade = self.db.query(Trade).filter_by(trade_id=trade_id).first()
        self.redirect(trade.show_url)


class WapPayNotifyHandler(APIPayHandler):
    @authenticated
    def post(self):
        logging.info("arguments:{}".format(self.request.arguments))

        payment_id = self.valid("trade_no")
        trade_id = self.valid("out_trade_no")
        fee = self.valid("total_amount", force_type=float)
        seller_id = self.valid("seller_id")
        trade_status = self.valid("trade_status", required=False)
        payor_id = self.valid("buyer_id", required=False) or ""
        created_at = self.valid("gmt_create", required=False) or ""
        payment_at = self.valid("gmt_payment", required=False) or ""

        # Add log.
        kwargs = {
          "trade_id": trade_id,
          "component": "wap_notify",
          "payload": self.request.arguments
        }
        LogTradeMgr.add(self.db, **kwargs)

        if self.errors:
            reason=self.errors.values()[0]
            raise HTTPError(422, "Arguments invalid", reason=reason)

        # Validate trade ID and total fee.
        trade = self.db.query(Trade).filter_by(trade_id=trade_id).first()
        if trade is None or float(fee) != trade.fee:
            # Notice is an exception notification, should be ignore.
            logging.info("exception notificaton, trade_id:{}".format(trade_id))
            return self.write("success")

        # Validate seller ID.
        if seller_id is not None and seller_id != config.ali_seller_id:
            # Notice is an exception notification, should be ignore.
            logging.info("exception notificaton, trade_id:{}".format(trade_id))
            return self.write("success")

        utcnow = util.utcnow()

        if trade_status in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
            kwargs = {
              "payor_id": payor_id,
              "status": trade_status,
              "created_at": created_at,
              "payment_at": payment_at,
              "trade": trade,
              "inserted_at": utcnow,
              "updated_at": utcnow,
              "payment_id": payment_id
            }
            payment = Payment(**kwargs)
            if trade_status == "TRADE_SUCCESS":
                trade.status = TradeStatus.SUCCESS
            else:
                # Trade finished, No refundable
                trade.status = TradeStatus.FINISHED

            self.db.add(payment)
            self.db.commit()
        elif trade_status == "TRADE_CLOSED":
            # TODO
            pass
        else:
            # TODO
            pass

        self.finish("success")


class WapRefundHandler(APIPayHandler):
    @gen.coroutine
    def get(self):
        trade_id = self.valid("trade_id")
        fee = self.valid("fee", force_type=float)

        if self.errors:
            reason=self.errors.values()[0]
            raise HTTPError(422, "Validation Failed", reason=reason)

        trade = self.db.query(Trade).filter_by(trade_id=trade_id).first()
        if trade is None:
            reason = "Invalid trade ID"
            raise HTTPError(422, "Validation Failed", reason=reason)

        if float(fee) != trade.fee:
            reason = "Your fee not equal total fee"
            raise HTTPError(422, "Validation Failed", reason=reason)

        if trade.status == TradeStatus.REFUND:
            reason = "Trade ID has been refund"
            raise HTTPError(422, "Validation Failed", reason=reason)

        alipay = AliWapPay(app_id=config.ali_app_id,
                           private_key_path=config.private_key_path,
                           sign_type= config.ali_sign_type
                           )
        query_string = alipay.refund(trade_id, fee)
        url = config.ali_gateway + "?" + query_string

        client = AsyncHTTPClient()
        response = yield client.fetch(url)

        resp_body = json.loads(response.body)
        refund_info = resp_body["alipay_trade_refund_response"]

        code = refund_info["code"]
        if code == "10000":
            # Refund successfully.
            trade.status = TradeStatus.REFUND
            trade.updated_at = util.utcnow()
            self.db.commit()
            refund_to_client = {"code": code}

        else:
            refund_to_client = {
                "code": code,
                "msg": refund_info["msg"],
                "sub_code": refund_info["sub_code"],
                "sub_msg": refund_info["sub_msg"]
            }

        self.finish({"refund": refund_to_client})