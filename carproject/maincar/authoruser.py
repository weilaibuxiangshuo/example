# -*- coding:utf-8 -*-
import functools,re
from tornado.web import HTTPError

from apps.system.models import WhiteList

from tools.resful_api import Resf as rf
from tools.jwt_api import JwtApi as jt

def newAuth(method):
    @functools.wraps(method)
    async def wrapper(self,*args, **kwargs):

        # ip限制
        ip = self.request.remote_ip
        globalRes = await self.application.objects.execute(WhiteList.select().where(WhiteList.is_global==True))
        if len(globalRes)>=1:
            try:
                ipRes = await self.application.objects.get(WhiteList, ip=ip)
            except WhiteList.DoesNotExist as e:
                return self.finish(rf().code(401))
            if not ipRes.is_through:
                return self.finish(rf().code(401))


        #判断是否带token返回
        try:
            reqAuth = self.request.headers['Authorization']
        except KeyError as e:
            return self.finish(rf().code(401))
            # return HTTPError(401)
        if reqAuth == "undefined" or (not reqAuth):
            return self.finish(rf().code(401))

        # 判断是否过期及token中是否有用户信息
        reqUser = jt().decode(reqAuth)
        if not reqUser:
            return self.finish(rf().code(401))

        #实例化redis获取用户信息
        rds = self.application.rds(2)
        userinfo = rds.get(reqUser['data'])
        if not userinfo:
            return self.finish(rf().code(401))
        self._current_user = userinfo.decode("utf8")

        #权限
        reqPath = self.request.uri.split("?")[0]
        whitePath = ["/index/"]

        if reqPath not in whitePath:
            is_per_through = 0
            perGet = rds.get(userinfo.decode("utf8")).decode("utf8")
            perList = eval(perGet)
            for p in perList:
                pl = p.split(":")
                reg = re.compile(eval(repr('^'+pl[0]+'$')))
                regR = reg.match(reqPath)
                methodR = self.request.method.lower()
                if regR and (methodR==pl[1]):
                    is_per_through = 1
            if is_per_through == 0:
                return self.finish(rf().set(403,"无权限访问"))

        return await method(self, *args, **kwargs)
    return wrapper

