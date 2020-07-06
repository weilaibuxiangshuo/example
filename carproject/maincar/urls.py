# -*- coding:utf-8 -*-

from tornado.web import URLSpec
from apps.system.urls import urlpatterns as systemurl

from maincar.handlers import (LoginHandler,IndexHandler)

urlpattern = [
    # URLSpec("/",LoginHandler,name="login"),
    URLSpec("/login/",LoginHandler,name="login"),
    URLSpec("/index/",IndexHandler,name="index"),
]

urlpattern += systemurl