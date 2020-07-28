# -*- coding:utf-8 -*-

from tornado.web import URLSpec
from apps.system.urls import urlpatterns as systemurl
from apps.record.urls import urlpatterns as recordurl

from maincar.handlers import (LoginHandler,IndexHandler,LogoutHandler)

urlpattern = [
    # URLSpec("/",LoginHandler,name="login"),
    URLSpec("/login/",LoginHandler,name="login"),
    URLSpec("/login/(\d+)/",LoginHandler),
    URLSpec("/index/",IndexHandler,name="index"),
    URLSpec("/logout/",LogoutHandler,name="logout"),
]

urlpattern += systemurl
urlpattern += recordurl