# -*- coding:utf-8 -*-
import peewee
from datetime import datetime

from maincar.mysqlconfig import asyncConnMysql

class BaseModel(peewee.Model):
    add_time = peewee.DateTimeField(default=datetime.now)
    class Meta:
        database = asyncConnMysql().database
