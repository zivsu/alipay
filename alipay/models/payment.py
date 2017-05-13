#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from models import BaseModel
import util


class Payment(BaseModel):
    __tablename__ = 'payment'

    payment_id = Column(VARCHAR(64), primary_key=True)
    payor_id = Column(VARCHAR(16))
    status = Column(VARCHAR(32), nullable=False)
    created_at = Column(VARCHAR(32), nullable=False)
    payment_at = Column(VARCHAR(32), nullable=False)
    trade_id = Column(VARCHAR(64), ForeignKey('trade.trade_id', name="trade_id_fk"), nullable=False)

    inserted_at = Column(INTEGER, nullable=False)
    updated_at = Column(INTEGER, nullable=False)

    trade = relationship("Trade", back_populates="payment")