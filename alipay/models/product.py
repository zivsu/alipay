#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, INTEGER
from sqlalchemy.orm import relationship

from models import BaseModel, DBSession
import util


class Product(BaseModel):
    __tablename__ = 'product'

    product_id = Column(INTEGER, primary_key=True, autoincrement="ignore_fk")
    title = Column(VARCHAR(256), nullable=False)
    descr = Column(VARCHAR(128))
    type = Column(TINYINT(1), nullable=False)

    inserted_at = Column(INTEGER, nullable=False)
    updated_at = Column(INTEGER, nullable=False)

    trade = relationship("Trade", uselist=False, back_populates="product")