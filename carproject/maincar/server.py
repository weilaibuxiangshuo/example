# -*- coding:utf-8 -*-
import os
from tornado import web,gen,ioloop

from maincar.mysqlconfig import asyncConnMysql
from maincar.urls import urlpattern
from maincar.redisconfig import BaseRedis

BasePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings={
    "static_path":os.path.join(BasePath,"static"),
    "static_url_prefix":"/static/",
    "template_path":os.path.join(BasePath,"templates"),
}


if __name__=="__main__":
    app = web.Application(urlpattern,**settings)
    app.listen(8099)
    app.objects = asyncConnMysql().newObject
    app.rds = BaseRedis
    # app.getRds = BaseRedis()
    io_loop = ioloop.IOLoop.current()
    io_loop.start()