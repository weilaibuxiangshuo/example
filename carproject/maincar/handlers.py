# -*- coding:utf-8 -*-

from tornado.web import RequestHandler,gen,authenticated,HTTPError
import peewee_async,json,hashlib,functools
from collections import deque


from apps.system.models import Menus,Permissions,Roles,Users,rolePermission

from tools.bcrpt_api import PasswordApi as pd
from tools.jwt_api import JwtApi as jt
from tools.resful_api import Resf as rf
from tools.decorator_api import dispatch_methods
from maincar.authoruser import newAuth



class LoginHandler(RequestHandler):

    async def get(self,num,*args,**kwargs):
        return self.finish(rf().code(200))

    async def post(self,*args,**kwargs):
        req = json.loads(self.request.body.decode("utf8"))
        try:
            oneUser = await self.application.objects.get(Users, username=req['username'])
        except Exception as e:
            raise HTTPError(401)
        #验证用户密码
        passwd = pd().checkpw(req['password'],oneUser.password)
        if passwd:
            userSha256 = hashlib.sha256(req['username'].encode('utf8')).hexdigest()
            #redis保存用户信息
            rds = self.application.rds(2)
            rds.set(userSha256,req['username'],ex=7200)
            resData = rf().code(200)
            resData['authorization'] = jt().encode(userSha256)
            return self.finish(resData)
        else:
            raise HTTPError(401)


@dispatch_methods([newAuth])
class IndexHandler(RequestHandler):
    async def get(self,*args,**kwargs):
        resData = rf().code(200)
        resData["username"] = self.current_user

        #获取对应角色
        getUser = await self.application.objects.get(Users,username=self.current_user)
        getRoles = await self.application.objects.execute(getUser.role)
        #权限集合
        permissionSet = set()
        #角色列表
        roleList=[]
        #获取所有权限
        for oneRole in getRoles:
            roleList.append(oneRole.title)
            getPers = await self.application.objects.execute(oneRole.permission)
            for onePer in getPers:
                permissionSet.add(onePer)


        #获取权限对应菜单
        menuSet = set()
        menuList = deque()
        for perSet in permissionSet:
            menuSet.add(perSet.menu)
            menuList.append(perSet.menu)

        #判断是否有上一级菜单,并获取
        while not (len(menuList) == 0):
            oneMenu = menuList.popleft()
            if oneMenu.sub:
                menuSet.add(oneMenu.sub)
                menuList.append(oneMenu.sub)

        #获取一级菜单
        parentMenus = [ i for i in menuSet if not i.sub]

        #排序方法
        def orderNum(arg):
            return arg["ord"]

        #按菜单顺序排列
        async def deep(data,level=1):
            num = level + 1
            tlist = []
            for one in data:
                if one not in menuSet:
                    continue
                res = {}
                childrens = await self.application.objects.execute(one.children)
                if not (len(childrens)==0):
                    res["children"] = await deep(childrens,num)
                res["level"] = level
                res["title"] = one.title
                res["icon"] = one.icon
                res["path"] = one.path
                res["code"] = one.code
                res["ord"] = one.ord
                res["role"] = roleList
                tlist.append(res)
            #进行排序
            orderList = sorted(tlist,key=orderNum)
            return orderList
        result = await deep(parentMenus)

        resData["menudata"] = result
        return self.finish(resData)


@dispatch_methods([newAuth])
class LogoutHandler(RequestHandler):
    async def post(self):
        rds = self.application.rds(2)
        userSha256 = hashlib.sha256(self.current_user.encode('utf8')).hexdigest()
        rds.delete(userSha256)
        return self.finish(rf().code(200))
