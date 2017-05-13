#!/usr/bin/env python
# coding:utf-8
import re
import calendar
import datetime


def is_vaild_email(email):
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_pattern.match(email) != None

def utcnow():
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple())
