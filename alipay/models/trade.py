#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, INTEGER, VARCHAR, DOUBLE
from sqlalchemy.orm import relationship

from models import BaseModel, DBSession
import util


class TradeMgr(object):
    @staticmethod
    def is_unique(db, trade_id):
        trade = db.query(Trade).filter_by(trade_id=trade_id).first()
        return (trade is None)


class Trade(BaseModel):
    __tablename__ = 'trade'

    trade_id = Column(VARCHAR(64), primary_key=True)
    fee = Column(DOUBLE, nullable=False)
    status = Column(TINYINT(1), nullable=False)
    channel = Column(TINYINT(1), nullable=False)
    show_url = Column(VARCHAR(256), nullable=False)
    timeout = Column(VARCHAR(6), nullable=False)
    product_id = Column(INTEGER, ForeignKey('product.product_id', name="product_id_fk"),
                        nullable=False)

    inserted_at = Column(INTEGER, nullable=False)
    updated_at = Column(INTEGER, nullable=False)

    product = relationship("Product", back_populates="trade")
    payment = relationship("Payment", uselist=False, back_populates="trade")