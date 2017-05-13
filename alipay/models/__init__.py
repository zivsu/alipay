#!/usr/bin/env python
# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import Query
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

import config

DB_URL = "{}://{}:{}@{}:{}/{}".format(
    config.db["driver"],
    config.db["username"],
    config.db["password"],
    config.db["host"],
    config.db["port"],
    config.db["database"]
)

BaseModel = declarative_base()
engine = create_engine(DB_URL)
if not database_exists(engine.url): create_database(engine.url)
DBSession = sessionmaker(bind=engine)

# print DBSession().query_property(Query)
# BaseModel.query = DBSession().query_property(Query)