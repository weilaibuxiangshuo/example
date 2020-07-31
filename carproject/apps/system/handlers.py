# -*- coding:utf-8 -*-
from tornado.web import RequestHandler, gen, authenticated
import peewee_async, json,hashlib

from apps.system.models import Menus, Permissions, Roles, Users, rolePermission,userRole,WhiteList
from apps.system.forms import MenusForm, PermissionsForm, RoleForm,UserForm,WhiteForm

from tools.bcrpt_api import PasswordApi as pd
from tools.resful_api import Resf as rf
from apps.system import utils
from tools.decorator_api import dispatch_methods
from maincar.authoruser import newAuth

@dispatch_methods(newAuth)
class MenuHandler(RequestHandler):
    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 判断search是否有值，有值返回搜索的值
        try:
            search = self.request.arguments['search'][0].decode("utf8")
        except Exception as f:
            search = None
        if search:
            allDataQuery.append((Menus.title == search))

        menusObj = await self.application.objects.execute(Menus.newData(allDataQuery).paginate(page, paginate_by=size).order_by(Menus.id.desc()))
        total = await self.application.objects.execute(Menus.newData(allDataQuery))
        list1 = []
        for menu in menusObj:
            dict1 = {
                "id": menu.id,
                "title": menu.title,
                "icon": menu.icon,
                "path": menu.path,
                "code": menu.code,
                "ord":menu.ord,
                "parent": menu.sub_id if menu.sub_id else "",
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        return self.finish(resData)

    # 添加菜单数据
    async def post(self, *args, **kwargs):
        resData = {}
        reqInfo = json.loads(self.request.body.decode("utf8"))
        # 转换格式为wtform-tornado支持
        reqInfo = {m: [n] for m, n in reqInfo.items()}
        valiForm = MenusForm(reqInfo)

        # 验证前端传值是否正确
        if valiForm.validate():
            obj = valiForm.data
            try:
                await self.application.objects.get(Menus, title=obj['title'])
                resData = rf().set(404, "失败菜单名已存在")
                return self.finish(resData)
            except Exception as f:
                dict1 = {
                    "title": obj['title'],
                    "icon": obj['icon'],
                    "path": obj['path'],
                    "code": obj['code'],
                    "ord":int(obj['ord']),
                }
                # 判断前端是否传父菜单id
                if reqInfo['parent'][0]:
                    dict1["sub_id"] = reqInfo['parent'][0]
                await self.application.objects.create(Menus, **dict1)
                resData = rf().code(201)
                self.finish(resData)
        else:
            resData = rf().code(404)
            resData['msg'] = valiForm.errors
            self.finish(resData)

    # 修改数据
    async def put(self, *args, **kwargs):
        resData = {}
        temp = json.loads(self.request.body.decode("utf8"))
        reqInfo = {m: [n] for m, n in temp.items()}
        reqvali = MenusForm(reqInfo)
        if reqvali.validate():
            try:
                oneEdit = await self.application.objects.get(Menus, id=reqInfo['id'])
            except Exception as e:
                self.finish(rf().set(404, "失败提交信息有误"))
            else:
                obj = reqvali.data
                oneEdit.title = obj['title']
                oneEdit.icon = obj['icon']
                oneEdit.path = obj['path']
                oneEdit.code = obj['code']
                oneEdit.ord = obj['ord']
                # 父菜单的值没有验证，直接从请求中获取并判断
                oneEdit.sub_id = None if str(reqInfo['parent'][0]).strip() == "" else int(
                    str(reqInfo['parent'][0]).strip())
                await self.application.objects.update(oneEdit)
                resData = rf().code(202)
        else:
            resData = rf().code(404)
            resData['msg'] = reqvali.errors
        return self.finish(resData)

    # 删除数据
    async def delete(self, *args, **kwargs):
        reqInfo = json.loads(self.request.body.decode("utf8"))
        for one in reqInfo['id']:
            one = int(one)
            await self.application.objects.execute(Menus.delete().where(Menus.id == one))
        self.finish(rf().code(204))

@dispatch_methods(newAuth)
class MenuListHandler(RequestHandler):
    async def get(self, *args, **kwargs):
        resData = {}
        await self.application.objects.execute(Menus.select().for_update())
        menusObj = await self.application.objects.execute(Menus.select())
        # 返回所有菜单信息
        list1 = []
        for menu in menusObj:
            dict1 = {
                "id": menu.id,
                "title": menu.title,
                "code": menu.code,
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        return self.finish(resData)

@dispatch_methods(newAuth)
class PermissionHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 判断search是否有值，有值返回搜索的值
        try:
            search = self.request.arguments['search'][0].decode("utf8")
        except Exception as f:
            search = None
        if search:
            allDataQuery.append((Permissions.title == search))

        permissionObj = await self.application.objects.execute(Permissions.newData(allDataQuery).paginate(page, paginate_by=size).order_by(Permissions.id.desc()))
        total = await self.application.objects.execute(Permissions.newData(allDataQuery))

        list1 = []
        for per in permissionObj:
            menuTitle = await self.application.objects.get(Menus, id=per.menu_id)
            dict1 = {
                "id": per.id,
                "title": per.title,
                "url": per.url,
                "method": eval(per.method),
                "menuid": menuTitle.id,
                "menu": menuTitle.title,
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        return self.finish(resData)

    # 添加权限
    async def post(self, *args, **kwargs):
        resData = {}
        reqData = json.loads(self.request.body.decode("utf8"))
        # 生成wtform-tornado验证格式
        reqDict = {m: [str(n)] for m, n in reqData.items()}
        valiDict = PermissionsForm(reqDict)
        if valiDict.validate():
            data = valiDict.data
            try:
                await self.application.objects.get(Permissions, title=data['title'])
                return self.finish(rf().set(404, "失败用户已存在"))
            except Exception as f:
                async with self.application.objects.atomic():
                    await self.application.objects.create(Permissions, title=data['title'], url=data['url'],
                                                          method=data['method'], menu_id=data['menu'])
                    resData = rf().code(201)
                    return self.finish(resData)
        else:
            resData = rf().code(404)
            resData['msg'] = valiDict.errors
            return self.finish(resData)

    # 修改数据
    async def put(self, *args, **kwargs):
        resData = {}
        temp = json.loads(self.request.body.decode("utf8"))
        reqInfo = {m: [str(n)] for m, n in temp.items()}
        reqvali = PermissionsForm(reqInfo)
        if reqvali.validate():
            try:
                oneEdit = await self.application.objects.get(Permissions, id=reqInfo['id'])
            except Exception as e:
                self.finish(rf().set(404, "失败提交信息有误"))
            else:
                obj = reqvali.data
                oneEdit.title = obj['title']
                oneEdit.url = obj['url']
                oneEdit.method = obj['method']
                oneEdit.menu_id = obj['menu']
                await self.application.objects.update(oneEdit)
                resData = rf().code(202)
        else:
            resData = rf().code(404)
            resData['msg'] =  reqvali.errors
        return self.finish(resData)

    # 删除数据
    async def delete(self, *args, **kwargs):
        reqInfo = json.loads(self.request.body.decode("utf8"))
        for one in reqInfo['id']:
            one = int(one)
            await self.application.objects.execute(Permissions.delete().where(Permissions.id == one))
        self.finish(rf().code(204))

@dispatch_methods(newAuth)
class PermissionMenuHandler(RequestHandler):
    # 获取最后一级所有菜单
    async def get(self, *args, **kwargs):
        resData = {}
        menuList = await self.application.objects.execute(Menus.select())
        resList = []
        for menu in menuList:
            # 判断是否有子菜单，并获取没有子菜单的菜单
            res = await self.application.objects.execute(menu.children)
            if len(res) == 0:
                temp = {
                    "menuid": menu.id,
                    "menutitle": menu.title,
                }
                resList.append(temp)
        resData = rf().code(200)
        resData['data'] = resList
        return self.finish(resData)

@dispatch_methods(newAuth)
class RolePermissionHandler(RequestHandler):

    # 返回菜单拼接权限的列表
    async def get(self, *args, **kwargs):
        permissionList = await self.application.objects.execute(Permissions.select())
        dataList = []
        dataSet = set()
        #获取底层菜单的权限
        for per in permissionList:
            if per.menu.title in dataSet:
                for m in dataList:
                    if m['title'] == per.menu.title:
                        subDict = {
                            'id': "permission" + "-" + str(per.id),
                            'title': per.title,
                        }
                        m['children'].append(subDict)
            else:
                dataSet.add(per.menu.title)
                dataDict = {
                    'id':per.menu.id,
                    'title':per.menu.title,
                    'children':[]
                }
                subDict = {
                    'id': "permission"+"-"+str(per.id),
                    'title': per.title,
                }
                dataDict['children'].append(subDict)
                dataList.append(dataDict)

        #获取菜单的层级列表
        menusList = await self.application.objects.execute(Menus.select())
        menuResList = []
        for menu in menusList:
            if not menu.sub_id:
                menuResList.append(menu)

        #根据底层菜单拼接权限
        dataJoin = await utils.deepRes(self, menuResList,0,dataList)
        resData1 = rf().code(200)
        resData1["data"] = dataJoin
        return self.finish(resData1)

@dispatch_methods(newAuth)
class RoleHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 判断search是否有值，有值返回搜索的值
        try:
            search = self.request.arguments['search'][0].decode("utf8")
        except Exception as f:
            search = None
        if search:
            allDataQuery.append((Roles.title == search))

        roleObj = await self.application.objects.execute(Roles.newData(allDataQuery).paginate(page, paginate_by=size).order_by(Roles.id.desc()))
        total = await self.application.objects.execute(Roles.newData(allDataQuery))
        list1 = []
        for one in roleObj:
            perList = []
            perObj = await self.application.objects.execute(one.permission)
            for t in perObj:
                temp = {
                    "id": "permission-" + str(t.id),
                    "title": t.title,
                }
                perList.append(temp)
            dict1 = {
                "id": one.id,
                "title": one.title,
                "permission": perList,
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        return self.finish(resData)

    async def post(self, *args, **kwargs):
        resData = {}
        reqData = json.loads(self.request.body.decode("utf8"))
        reqList = {m: [str(n)] for m, n in reqData.items()}
        result = RoleForm(reqList)
        if result.validate():
            try:
                await self.application.objects.get(Roles, title=reqData['title'])
                return self.finish(rf().set(404, "失败用户已存在"))
            except Roles.DoesNotExist as e:
                # 过滤出权限id列表
                perList = [int(str(i).split('permission-')[1]) for i in reqData["permission"] if
                           str(i).startswith("permission-")]
                async with self.application.objects.atomic():
                    roleOne = await self.application.objects.create(Roles, title=reqData['title'])
                    if not len(perList) == 0:
                        for c in perList:
                            # 给角色添加权限
                            await self.application.objects.create(rolePermission, roles_id=roleOne.id, permissions_id=c)
                return self.finish(rf().code(201))
        else:
            resData = rf().code(404)
            resData['msg'] = result.errors
            return self.finish(resData)

    # 修改数据
    async def put(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode("utf8"))
        reqList = {m: [str(n)] for m, n in reqData.items()}
        result = RoleForm(reqList)
        if result.validate():
            valiData = result.data
            try:
                oneRole = await self.application.objects.get(Roles, id=reqData['id'])
            except Roles.DoesNotExist as e:
                return self.finish(rf().set(404, "失败用户不存在"))
            async with self.application.objects.atomic():
                oneRole.title = valiData['title']
                await self.application.objects.update(oneRole)
                #删除原来角色对应权限
                await self.application.objects.execute(rolePermission.delete().where(rolePermission.roles_id == oneRole.id))
                # 过滤出权限id列表
                perList = [int(str(i).split('permission-')[1]) for i in reqData["permission"] if
                           str(i).startswith("permission-")]
                if not len(perList) == 0:
                    for c in perList:
                        # 给角色添加权限
                        await self.application.objects.create(rolePermission, roles_id=oneRole.id, permissions_id=c)
                return self.finish(rf().code(202))
        else:
            resData = rf().code(404)
            resData['msg'] = result.errors
            return self.finish(resData)

    # 删除数据
    async def delete(self, *args, **kwargs):
        reqInfo = json.loads(self.request.body.decode("utf8"))
        for one in reqInfo['id']:
            one = int(one)
            await self.application.objects.execute(Roles.delete().where(Roles.id == one))
        self.finish(rf().code(204))

@dispatch_methods(newAuth)
class UserRoleHandler(RequestHandler):
    """
    返回所有角色列表
    """
    async def get(self,*args,**kwargs):
        roleList = await self.application.objects.execute(Roles.select())
        resList = []
        for role in roleList:
            dict1 = {
                "id":role.id,
                "title":role.title,
            }
            resList.append(dict1)
        resData = rf().code(200)
        resData['data'] = resList
        return self.finish(resData)

@dispatch_methods(newAuth)
class UserHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 判断search是否有值，有值返回搜索的值
        try:
            search = self.request.arguments['search'][0].decode("utf8")
        except Exception as f:
            search = None
        if search:
            allDataQuery.append((Users.username == search))

        userAllObj = await self.application.objects.execute(
            Users.newData(allDataQuery).paginate(page, paginate_by=size).order_by(Users.id.desc()))
        total = await self.application.objects.execute(Users.newData(allDataQuery))

        list1 = []
        for one in userAllObj:
            roleList = []
            #获取跟用户关联的角色
            roleObj = await self.application.objects.execute(one.role)
            for t in roleObj:
                temp = {
                    "id": t.id,
                    "title": t.title,
                }
                roleList.append(temp)
            dict1 = {
                "id": one.id,
                "username": one.username,
                "is_superuser":one.is_superuser,
                "role": roleList,
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        return self.finish(resData)

    #添加用户
    async def post(self,*args,**kwargs):

        reqData = json.loads(self.request.body.decode("utf8"))
        # 生成wtform-tornado验证格式
        reqDict = {m: [str(n)] for m, n in reqData.items()}
        valiDict = UserForm(reqDict)
        if valiDict.validate():
            newData = valiDict.data
            try:
                await self.application.objects.get(Users, username=reqData['username'])
                resData = rf().set(404,"失败用户已存在")
                return self.finish(resData)
            except Users.DoesNotExist as e:
                async with self.application.objects.atomic():
                    newData["password"] = pd().hashed(newData['password'])
                    oneUser = await self.application.objects.create(Users,**newData)
                    for n in reqData['checkedData']:
                        await self.application.objects.create(userRole,users_id=oneUser.id,roles_id=n)
                return self.finish(rf().code(201))
        else:
            resData = rf().code(404)
            resData['msg'] = valiDict.errors
            return self.finish(resData)


    # 修改数据
    async def put(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode("utf8"))
        reqList = {m: [str(n)] for m, n in reqData.items()}
        valiDict = UserForm(reqList)
        if valiDict.validate():
            valiData = valiDict.data
            try:
                oneUser = await self.application.objects.get(Users, id=reqData['id'])
            except Users.DoesNotExist as e:
                return self.finish(rf().set(404, "失败用户不存在"))
            pwd_bcrpt = pd().hashed(valiData['password'])
            # oneUser.password = hashlib.sha256(valiData['password'].encode('utf8')).hexdigest()
            async with self.application.objects.atomic():
                params = {
                    "username":valiData['username'],
                    "password":pwd_bcrpt,
                }
                await self.application.objects.execute(Users.update(**params).where(Users.id == oneUser.id))

                #删除对应角色
                await self.application.objects.execute(userRole.delete().where(userRole.users_id == oneUser.id))
                #过滤出权限id列表
                if not len(reqData["checkedData"] ) == 0:
                    for c in reqData["checkedData"]:
                        # 给角色添加权限
                        await self.application.objects.create(userRole, users_id=oneUser.id, roles_id=c)
            return self.finish(rf().code(202))
        else:
            resData = rf().code(404)
            resData['msg'] = valiDict.errors
            return self.finish(resData)

    # 删除数据
    async def delete(self, *args, **kwargs):
        reqInfo = json.loads(self.request.body.decode("utf8"))
        for one in reqInfo['id']:
            one = int(one)
            await self.application.objects.execute(Users.delete().where(Users.id == one))
        self.finish(rf().code(204))


@dispatch_methods([newAuth])
class WhiteListHandler(RequestHandler):
    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)
        # 判断search是否有值，有值返回搜索的值
        try:
            search = self.request.arguments['search'][0].decode("utf8")
        except Exception as f:
            search = None
        if search:
            allDataQuery.append((WhiteList.ip == search))

        ipAllObj = await self.application.objects.execute(
            WhiteList.newData(allDataQuery).paginate(page, paginate_by=size).order_by(WhiteList.id.desc()))
        total = await self.application.objects.execute(WhiteList.newData(allDataQuery))

        list1 = []
        is_global = []
        for one in ipAllObj:
            dict1 = {
                "id": one.id,
                "ip": one.ip,
                "is_through":"1" if one.is_through else "2" ,
            }
            if one.is_global:
                is_global.append(one)
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        resData["is_global"] = True if len(is_global)>=1 else False
        return self.finish(resData)

    #添加IP
    async def post(self,*args,**kwargs):

        reqData = json.loads(self.request.body.decode("utf8"))
        # 生成wtform-tornado验证格式
        reqDict = {m: [str(n)] for m, n in reqData.items()}
        valiDict = WhiteForm(reqDict)
        if valiDict.validate():
            newData = valiDict.data
            through = False if reqData["is_through"] == "2" else True
            try:
                await self.application.objects.get(WhiteList, ip=newData['ip'])
                resData = rf().set(404,"失败IP已存在")
                return self.finish(resData)
            except WhiteList.DoesNotExist as e:
                async with self.application.objects.atomic():
                    await self.application.objects.create(WhiteList,ip=newData['ip'],is_through=through)
                return self.finish(rf().code(201))
        else:
            resData = rf().code(404)
            resData['msg'] = valiDict.errors
            return self.finish(resData)


    # 修改IP
    async def put(self, *args, **kwargs):

        reqData = json.loads(self.request.body.decode("utf8"))
        # 生成wtform-tornado验证格式
        reqDict = {m: [str(n)] for m, n in reqData.items()}
        valiDict = WhiteForm(reqDict)
        if valiDict.validate():
            newData = valiDict.data
            through = False if reqData["is_through"] == "2" else True
            try:
                oneIp = await self.application.objects.get(WhiteList, id=reqData['id'])
            except WhiteList.DoesNotExist as e:
                resData = rf().code(404)
                return self.finish(resData)
            async with self.application.objects.atomic():
                oneIp.ip = newData['ip']
                oneIp.is_through = through
                await self.application.objects.update(oneIp)
            return self.finish(rf().code(202))
        else:
            resData = rf().code(404)
            resData['msg'] = valiDict.errors
            return self.finish(resData)

    # 删除IP
    async def delete(self, *args, **kwargs):
        reqInfo = json.loads(self.request.body.decode("utf8"))
        for one in reqInfo['id']:
            one = int(one)
            await self.application.objects.execute(WhiteList.delete().where(WhiteList.id == one))
        self.finish(rf().code(204))


class WhiteListSetHandler(RequestHandler):
    async def post(self):
        reqData = json.loads(self.request.body.decode("utf8"))
        # 生成wtform-tornado验证格式
        btncontrol = False if reqData["btncontrol"] == "2" else True
        res = await self.application.objects.execute(WhiteList.update(is_global=btncontrol))
        if not res:
            resData = rf().set(404, "IP限制开启失败")
            return self.finish(resData)
        return self.finish(rf().code(202))