#!/usr/bin/env python
# coding=utf-8
import json

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, INTEGER, TEXT

import util
from models import BaseModel


class LogTradeMgr(object):
    @staticmethod
    def add(db, **kwargs):
        # We need to hash down the payload if there is one.
        if 'payload' in kwargs and kwargs['payload'] is not None:
            kwargs['payload'] = json.dumps(dict(kwargs.get('payload')))

        kwargs["inserted_at"] = util.utcnow()
        log_trade = LogTrade(**kwargs)
        db.add(log_trade)
        db.commit()


class LogTrade(BaseModel):
    __tablename__ = 'log_trade'

    id = Column(INTEGER, autoincrement=True, primary_key=True)
    trade_id = Column(VARCHAR(64), nullable=False)
    component = Column(VARCHAR(50), nullable=False)
    payload = Column(TEXT)
    inserted_at = Column(INTEGER, nullable=False)