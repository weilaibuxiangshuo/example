# -*- coding:utf-8 -*-
from tornado.web import HTTPError
import functools

from tools.resful_api import Resf as rf
from tools.jwt_api import JwtApi as jt

def newAuth(method):
    @functools.wraps(method)
    async def wrapper(self,*args, **kwargs):
        # print(self.request.headers['Authorization'],"ooo")
        #判断是否带token返回

        try:
            reqAuth = self.request.headers['Authorization']
        except Exception as e:
            self.finish(rf().code(401))

        # 判断是否过期及token中是否有用户信息
        reqUser = jt().decode(reqAuth)
        if not reqUser:
            return self.finish(rf().code(401))

        #实例化redis获取用户信息
        rds = self.application.rds(2)
        userinfo = rds.get(reqUser['data'])
        # print("搞笑",userinfo)
        if not userinfo:
            return self.finish(rf().code(401))
        self._current_user = userinfo.decode("utf8")
        return await method(self, *args, **kwargs)
    return wrapper

