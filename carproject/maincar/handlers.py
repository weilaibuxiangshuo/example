# -*- coding:utf-8 -*-

from tornado.web import RequestHandler,gen,authenticated
import peewee_async,json

from apps.system.models import Menus,Permissions,Roles,Users,rolePermission

from tools.bcrpt_api import PasswordApi as pd
from tools.jwt_api import JwtApi as jt
from tools.resful_api import Resf as rf

class LoginHandler(RequestHandler):
    async def get(self,*args,**kwargs):
        # res = await self.application.objects.get(rolePermission,id=202)
        # print(res.permissions_id,type(res.permissions_id))
        # result = await gen.multi_future([self.application.objects.execute(i.people_goods) for i in res])
        # print(Jwt().encode("admin"),rep)

        return self.finish(rf().code(200))

    async def post(self,*args,**kwargs):
        print("111")
        # print(self.request.body.decode("utf8"))
        resData = {}
        req = json.loads(self.request.body.decode("utf8"))
        try:
            oneUser = await self.application.objects.get(Users, username=req['username'])
        except Exception as e:
            self.set_status(401)
            self.finish(rf.code(401))
        passwd = pd().checkpw(req['password'],oneUser.password)
        if passwd:
            resData['authorization'] = jt().encode(req['username'])
        resData.update(rf.code(200))
        return self.finish(resData)



class IndexHandler(RequestHandler):
    async def get(self,*args,**kwargs):
        # print("index")
        # print(self.request.headers['Authorization'])
        #判断是否带token返回
        try:
            req = self.request.headers['Authorization']
        except Exception as e:
            self.set_status(401)
            self.finish(rf.code(401))
        # 判断是否过期及token中是否有用户信息
        try:
            reqUser = jt().decode(self.request.headers['Authorization'])
            user = await self.application.objects.get(Users, username=reqUser['data'])
        except Exception as m:
            self.set_status(401)
            self.finish(rf.code(401))
        resData = {"username":user.username}
        resData.update(rf.code(200))

        return self.finish(resData)
