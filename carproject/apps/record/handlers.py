# -*- coding:utf-8 -*-
from tornado.web import RequestHandler
import redis, uuid, json, datetime, time

from apps.record.models import Records
from apps.system.models import Users
from apps.record.forms import RecordsForm
from apps.record.utils import RedisGroup

from tools.resful_api import Resf as rf
from tools.decorator_api import dispatch_methods
from maincar.authoruser import newAuth


@dispatch_methods(newAuth)
class ManagementHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 重要条件：判断是否有时间，所有查询必须有时间
        try:
            timeList = self.request.arguments['timeinfo'][0].decode('utf8').split("-")
            allDataQuery.append((Records.date_group.year == timeList[0]))
            allDataQuery.append((Records.date_group.month == timeList[1]))
            allDataQuery.append((Records.date_group.day == timeList[2]))
        except Exception as f:
            timeList = None

        # 时间为空返回空信息
        if not timeList:
            resData = rf().code(404)
            resData["data"] = []
            resData["total"] = 0
            return self.finish(resData)

        # 判断搜索是否有值
        try:
            searchgroup = self.request.arguments['searchgroup'][0].decode("utf8")
            searchcontext = self.request.arguments['searchcontext'][0].decode("utf8")
        except Exception as f:
            searchgroup = None
            searchcontext = None
        if searchgroup and searchcontext:
            searchDict = {
                "1": Records.onlyid,
                "2": Records.account,
                "3": Records.name,
                "4": Records.amount,
                "5": Records.cardnum,
            }
            if searchgroup == "4":
                try:
                    searchcontext = int(searchcontext)
                except Exception as e:
                    searchcontext = 0
            allDataQuery.append((searchDict[searchgroup] == searchcontext))

        # 加条件只返回当前用户数据
        allDataQuery.append((Records.user_group == self.current_user))

        # 判断allDataQuery是否有值
        dataObj = await self.application.objects.execute(
            Records.newdata(allDataQuery).paginate(page, paginate_by=size).order_by(Records.id.desc()))

        total = await self.application.objects.execute(Records.newdata(allDataQuery))
        newSum = sum([int(nn.amount) for nn in await self.application.objects.execute(Records.newdata(allDataQuery))])

        list1 = []
        for one in dataObj:
            dict1 = {
                "id": one.id,
                "onlyid": one.onlyid,
                "name": one.name,
                "cardclass": one.cardclass,
                "cardnum": one.cardnum,
                "amount": int(one.amount),
                "account": one.account,
                "remark": one.remark,
                "is_freeze": one.is_freeze,
                "is_lock": one.is_lock,
                "is_confirm": one.is_confirm,
                "date_group": one.date_group.strftime('%Y-%m-%d'),
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        resData["sum"] = newSum
        return self.finish(resData)

    # 添加记录
    async def post(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode('utf8'))
        getUser = await self.application.objects.get(Users, username=self.current_user)
        uuidList = str(uuid.uuid1()).split("-")
        # 生成订单号
        onlyId = "".join(str(datetime.datetime.now().timestamp()).split(".") + uuidList)
        dict1 = {
            "onlyid": onlyId,
            "name": reqData["name"],
            "cardclass": reqData["cardclass"],
            "cardnum": reqData["cardnum"],
            "amount": int(reqData["amount"]),
            "account": reqData["account"],
            "remark": reqData["remark"],
            "user_group": getUser.username,
            "date_group": datetime.datetime.strptime(reqData["timeinfo"], "%Y-%m-%d"),
        }
        await self.application.objects.create(Records, **dict1)
        return self.finish(rf().code(201))

    # 修改记录
    async def put(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode('utf8'))

        # 获取redis验证信息
        rds = RedisGroup(self)
        rdsInfo = await rds.get(reqData)
        if rdsInfo:
            return self.finish(rdsInfo)

        # 修改记录
        recordData = {m: [n] if isinstance(n, str) else [str(n)] for m, n in reqData.items()}
        valiData = RecordsForm(recordData)
        if valiData.validate():
            getRecord = await self.application.objects.get(Records, id=reqData["id"], onlyid=reqData["onlyid"])
            valiUuid = getRecord.uuidnum
            val = valiData.data
            _dict1 = {
                "cardclass": val["cardclass"],
                "name": val["name"],
                "account": val["account"],
                "amount": int(val["amount"]),
                "cardnum": val["cardnum"],
                "remark": reqData["remark"],
                "last_time": datetime.datetime.now()
            }
            resSql = await self.application.objects.execute(Records.update(**_dict1, uuidnum=uuid.uuid1()).where(
                (Records.id == reqData["id"]) & (Records.onlyid == reqData["onlyid"]) & (Records.uuidnum == valiUuid)))
            if resSql == 0:
                return self.finish(rf().code(404))
            return self.finish(rf().code(202))
        else:
            resData = rf().set(404, "更新失败")
            resData["msg"] = valiData.errors

    # 删除数据
    async def delete(self, *args, **kwargs):

        reqData = json.loads(self.request.body.decode("utf8"))

        # 实例化redis
        rds = RedisGroup(self)

        for one in reqData['data']:
            # 获取redis验证信息
            rdsInfo = await rds.get(one)
            if rdsInfo:
                return self.finish(rdsInfo)

            await self.application.objects.execute(
                Records.delete().where((Records.id == one["id"]) & (Records.onlyid == one["onlyid"])))
            rds.delete()
        self.finish(rf().set(204, "删除成功"))


@dispatch_methods(newAuth)
class ManagementStatusHandler(RequestHandler):

    # 点击冻结
    async def post(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode('utf8'))

        # 验证redis信息
        rds = RedisGroup(self)
        rdsInfo = await rds.set(reqData)
        if rdsInfo:
            return self.finish(rdsInfo)

        # 判断用户id是否存在
        try:
            oneRecord = await self.application.objects.get(Records, id=reqData["id"], onlyid=reqData["onlyid"])
            validata = oneRecord.uuidnum
        except Exception as e:
            rds.delete()
            return self.finish(rf().code(404))

        # 判断初始状态是否为确定
        if oneRecord.is_confirm:
            rds.delete()
            return self.finish(rf().set(404, "失败记录已确定"))

        # 更改冻结状态
        if reqData["is_freeze"]:
            async with self.application.objects.atomic():
                result = await self.application.objects.execute(
                    Records.update(is_freeze=reqData["is_freeze"], uuidnum=uuid.uuid1(),
                                   lock_user=self.current_user).where(
                        (Records.id == reqData["id"]) & (Records.uuidnum == validata) & (Records.is_confirm == False)))
                if result == 0:
                    rds.delete()
                    return self.finish(rf().code(404))
            return self.finish(rf().set(202, "操作成功"))
        else:
            async with self.application.objects.atomic():
                result = await self.application.objects.execute(
                    Records.update(is_freeze=reqData["is_freeze"], uuidnum=uuid.uuid1(),
                                   lock_user=self.current_user).where(
                        (Records.id == reqData["id"]) & (Records.uuidnum == validata) & (Records.is_confirm == False)))
                if result == 0:
                    return self.finish(rf().code(404))
            rds.delete()
            return self.finish(rf().set(202, "操作成功"))


@dispatch_methods(newAuth)
class EventProcessHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 重要条件：判断是否有时间，所有查询必须有时间
        try:
            timeList = self.request.arguments['timeinfo'][0].decode('utf8').split("-")
            allDataQuery.append((Records.date_group.year == timeList[0]))
            allDataQuery.append((Records.date_group.month == timeList[1]))
            allDataQuery.append((Records.date_group.day == timeList[2]))
        except Exception as f:
            timeList = None

        # 时间为空返回空信息
        if not timeList:
            resData = rf().code(404)
            resData["data"] = []
            resData["total"] = 0
            return self.finish(resData)

        # 获取前端传递的过滤
        try:
            filterdisplay = self.request.arguments['filterdisplay'][0].decode("utf8")
        except Exception as f:
            filterdisplay = None

        if filterdisplay:
            if filterdisplay == "5":
                allDataQuery.append((Records.is_lock == True))
                allDataQuery.append((Records.lock_user == self.current_user))
            elif filterdisplay == "6":
                allDataQuery.append((Records.is_confirm == True))
                allDataQuery.append((Records.operator == self.current_user))
            else:
                filterDict = {
                    "1": (Records.is_lock == False),
                    "2": (Records.is_lock == True),
                    "3": (Records.is_confirm == False),
                    "4": (Records.is_confirm == True),
                }
                allDataQuery.append(filterDict[filterdisplay])

        # 判断搜索是否有值
        try:
            searchgroup = self.request.arguments['searchgroup'][0].decode("utf8")
            searchcontext = self.request.arguments['searchcontext'][0].decode("utf8")
        except Exception as f:
            searchgroup = None
            searchcontext = None
        if searchgroup and searchcontext:
            searchDict = {
                "1": Records.onlyid,
                "2": Records.account,
                "3": Records.name,
                "4": Records.amount,
                "5": Records.cardnum,
            }
            if searchgroup == "4":
                try:
                    searchcontext = int(searchcontext)
                except Exception as e:
                    searchcontext = 0
            allDataQuery.append((searchDict[searchgroup] == searchcontext))

        # 判断allDataQuery是否有值
        dataObj = await self.application.objects.execute(
            Records.newdata(allDataQuery).paginate(page, paginate_by=size).order_by(Records.id.desc()))

        total = await self.application.objects.execute(Records.newdata(allDataQuery))
        newSum = sum([int(nn.amount) for nn in await self.application.objects.execute(Records.newdata(allDataQuery))])

        list1 = []
        for one in dataObj:
            # 判断是否是当前用户在操作
            if not one.is_freeze and not one.is_lock:
                is_if_show = True
            else:
                if one.lock_user == self.current_user or one.operator == self.current_user:
                    is_if_show = True
                else:
                    is_if_show = False

            dict1 = {
                "id": one.id,
                "onlyid": one.onlyid,
                "name": one.name,
                "cardclass": one.cardclass,
                "cardnum": one.cardnum,
                "amount": int(one.amount),
                "account": one.account,
                "remark": one.remark,
                "is_freeze": one.is_freeze,
                "is_confirm": one.is_confirm,
                "is_lock": one.is_lock,
                "user_group": one.user_group,
                "lock_user": one.lock_user,
                "date_group": one.date_group.strftime('%Y-%m-%d'),
                "is_if_show": is_if_show,
                "operator": self.current_user if is_if_show else (one.operator if one.operator else one.lock_user),
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        resData["sum"] = newSum
        return self.finish(resData)


@dispatch_methods(newAuth)
class EventProcessStatusHandler(RequestHandler):

    # 锁定操作
    async def post(self, *args, **kwargs):

        reqData = json.loads(self.request.body.decode('utf8'))

        # 获取redis验证信息
        rds = RedisGroup(self)
        rdsInfo = await rds.set(reqData)
        if rdsInfo:
            return self.finish(rdsInfo)

        try:
            oneRecord = await self.application.objects.get(Records, id=reqData["id"], onlyid=reqData["onlyid"])
            validata = oneRecord.uuidnum
        except Exception as e:
            rds.delete()
            return self.finish(rf().code(404))

        # 判断初始状态是否为确定
        if oneRecord.is_confirm:
            rds.delete()
            return self.finish(rf().set(404, "失败记录已确定"))

        # 判断初始状态是否为确定
        if oneRecord.is_freeze:
            return self.finish(rf().set(404, "其它用户已锁定"))

        # 更改锁定状态
        if reqData["is_lock"]:
            async with self.application.objects.atomic():
                result = await self.application.objects.execute(
                    Records.update(is_lock=reqData["is_lock"], uuidnum=uuid.uuid1(),
                                   lock_user=self.current_user).where(
                        (Records.id == reqData["id"]) & (Records.uuidnum == validata) & (Records.is_confirm == False)))
                if result == 0:
                    rds.delete()
                    return self.finish(rf().code(404))
            return self.finish(rf().set(202, "操作成功"))
        else:
            async with self.application.objects.atomic():
                result = await self.application.objects.execute(
                    Records.update(is_lock=reqData["is_lock"], uuidnum=uuid.uuid1(),
                                   lock_user=self.current_user).where(
                        (Records.id == reqData["id"]) & (Records.uuidnum == validata) & (Records.is_confirm == False)))
                if result == 0:
                    return self.finish(rf().code(404))
            rds.delete()
            return self.finish(rf().set(202, "操作成功"))


@dispatch_methods(newAuth)
class EventProcessConfirmHandler(RequestHandler):

    # 点击确定
    async def post(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode('utf8'))

        # 获取redis验证信息
        rds = RedisGroup(self)
        rdsInfo = await rds.get(reqData)
        if rdsInfo:
            return self.finish(rdsInfo)

        # 先判断请求用户数据是否存在
        try:
            oneRecord = await self.application.objects.get(Records, id=reqData["id"], onlyid=reqData["onlyid"])
            validata = oneRecord.uuidnum
        except Exception as e:
            return self.finish(rf().code(404))

        # 判断初始状态是否为冻结，如果不是，取消操作
        if not oneRecord.is_lock:
            return self.finish(rf().code(404))

        async with self.application.objects.atomic():
            result = await self.application.objects.execute(
                Records.update(uuidnum=uuid.uuid1(), lock_user=None, is_confirm=True,
                               operator=self.current_user).where(
                    (Records.id == reqData["id"]) & (Records.uuidnum == validata)))
            if result == 0:
                return self.finish(rf().code(404))
        rds.delete()
        return self.finish(rf().set(202, "操作成功"))

@dispatch_methods(newAuth)
class EventProcessFailHandler(RequestHandler):
    async def post(self):
        resData = {}
        reqData = json.loads(self.request.body.decode('utf8'))
        try:
            getOnlyid = await self.application.objects.get(Records, onlyid=reqData["onlyid"])
        except Exception as e:
            return self.finish(rf().set(404,"信息有误"))

        if getOnlyid.is_fail:
            return self.finish(rf().set(404, "该信息已提交过"))

        getOnlyid.is_fail = True
        getOnlyid.spare1 = self.current_user
        res = await self.application.objects.update(getOnlyid)
        if res == 0:
            return self.finish(rf().set(404, "操作失败"))
        return self.finish(rf().code(202))

@dispatch_methods(newAuth)
class DisplaystandHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)

        # 重要条件：判断是否有时间，所有查询必须有时间
        try:
            timeList = self.request.arguments['timeinfo'][0].decode("utf8")
            timeList = json.loads(timeList)
            t1 = datetime.datetime.strptime(timeList[0], '%Y-%m-%d')
            t2 = datetime.datetime.strptime(timeList[1], '%Y-%m-%d')
            allDataQuery.append((Records.date_group.between(t1, t2)))
        except Exception as f:
            timeList = None

        # 时间为空返回空信息
        if not timeList:
            resData = rf().code(200)
            resData["data"] = []
            resData["total"] = 0
            return self.finish(resData)

        # 判断搜索是否有值
        try:
            searchgroup = self.request.arguments['searchgroup'][0].decode("utf8")
            searchcontext = self.request.arguments['searchcontext'][0].decode("utf8")
        except Exception as f:
            searchgroup = None
            searchcontext = None
        if searchgroup and searchcontext:
            searchDict = {
                "1": Records.onlyid,
                "2": Records.account,
                "3": Records.name,
                "4": Records.amount,
                "5": Records.cardnum,
                "6": Records.operator,
                "7": Records.user_group,
                "8": Records.remark,
            }
            if searchgroup == "4":
                try:
                    searchcontext = int(searchcontext)
                except Exception as e:
                    searchcontext = 0
            allDataQuery.append((searchDict[searchgroup] == searchcontext))

        # 获取前端传递的过滤
        try:
            filterdisplay = self.request.arguments['filterdisplay'][0].decode("utf8")
        except Exception as f:
            filterdisplay = None

        if filterdisplay:
            if filterdisplay == "1":
                allDataQuery.append((Records.is_fail == False))
            elif filterdisplay == "2":
                allDataQuery.append((Records.is_fail == True))


        #显示所有已确定的数据
        allDataQuery.append((Records.is_confirm == True))

        # 判断allDataQuery是否有值
        total = await self.application.objects.execute(Records.newdata(allDataQuery))
        newSum = sum([int(nn.amount) for nn in await self.application.objects.execute(Records.newdata(allDataQuery))])
        dataObj = await self.application.objects.execute(
            Records.newdata(allDataQuery).paginate(page, paginate_by=size).order_by(Records.id.desc()))

        list1 = []
        for one in dataObj:
            # 判断是否是当前用户在操作
            if not one.is_freeze and not one.is_lock:
                is_if_show = True
            else:
                if one.lock_user == self.current_user or one.operator == self.current_user:
                    is_if_show = True
                else:
                    is_if_show = False

            dict1 = {
                "id": one.id,
                "onlyid": one.onlyid,
                "name": one.name,
                "cardclass": one.cardclass,
                "cardnum": one.cardnum,
                "amount": int(one.amount),
                "account": one.account,
                "remark": one.remark,
                "is_freeze": one.is_freeze,
                "is_confirm": one.is_confirm,
                "is_lock": one.is_lock,
                "user_group": one.user_group,
                "lock_user": one.lock_user,
                "spare1": one.spare1,
                "date_group": one.date_group.strftime('%Y-%m-%d'),
                "is_if_show": is_if_show,
                "operator": self.current_user if is_if_show else (one.operator if one.operator else one.lock_user),
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        resData["sum"] = newSum
        return self.finish(resData)


    # 删除数据
    async def delete(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode("utf8"))

        for one in reqData['data']:
            await self.application.objects.execute(
                Records.delete().where((Records.id == one["id"]) & (Records.onlyid == one["onlyid"])))
        self.finish(rf().set(204, "删除成功"))

@dispatch_methods(newAuth)
class FailSearchHandler(RequestHandler):

    # 分页返回数据
    async def get(self, page, size, *args, **kwargs):

        # 所有过滤或查询的列表集合
        allDataQuery = []
        page = int(page)
        size = int(size)
        # 重要条件：判断是否有时间，所有查询必须有时间
        try:
            timeList = self.request.arguments['timeinfo'][0].decode("utf8")
            timeList = json.loads(timeList)
            t1 = datetime.datetime.strptime(timeList[0],'%Y-%m-%d')
            t2 = datetime.datetime.strptime(timeList[1],'%Y-%m-%d')
            allDataQuery.append((Records.date_group.between(t1,t2)))
        except Exception as f:
            timeList = None

        # 时间为空返回空信息
        if not timeList:
            resData = rf().code(200)
            resData["data"] = []
            resData["total"] = 0
            return self.finish(resData)

        # 判断搜索是否有值
        try:
            searchgroup = self.request.arguments['searchgroup'][0].decode("utf8")
            searchcontext = self.request.arguments['searchcontext'][0].decode("utf8")
        except Exception as f:
            searchgroup = None
            searchcontext = None
        if searchgroup and searchcontext:
            if searchgroup in ["3","4","5","6"]:
                searchDict = {
                    "3": Records.account,
                    "4": Records.name,
                    "5": Records.amount,
                    "6": Records.cardnum,
                }
                if searchgroup == "4":
                    try:
                        searchcontext = int(searchcontext)
                    except Exception as e:
                        searchcontext = 0
                allDataQuery.append((searchDict[searchgroup] == searchcontext))
            if searchgroup == "1":
                allDataQuery.append((Records.onlyid == searchcontext))
                allDataQuery.append((Records.is_fail == False))
            if searchgroup == "2":
                allDataQuery.append((Records.onlyid == searchcontext))
                allDataQuery.append((Records.is_fail == True))

        # 获取前端传递的过滤
        try:
            filterdisplay = self.request.arguments['filterdisplay'][0].decode("utf8")
        except Exception as f:
            filterdisplay = None

        if filterdisplay:
            if filterdisplay == "1":
                allDataQuery.append((Records.is_fail == False))
            elif filterdisplay == "2":
                allDataQuery.append((Records.is_fail == True))


        #显示所有已确定且当前用户的数据
        allDataQuery.append((Records.is_confirm == True))
        allDataQuery.append((Records.user_group == self.current_user))

        # 判断allDataQuery是否有值
        total = await self.application.objects.execute(Records.newdata(allDataQuery))
        newSum = sum([int(nn.amount) for nn in await self.application.objects.execute(Records.newdata(allDataQuery))])
        dataObj = await self.application.objects.execute(
            Records.newdata(allDataQuery).paginate(page, paginate_by=size).order_by(Records.id.desc()))

        list1 = []
        for one in dataObj:
            dict1 = {
                "id": one.id,
                "onlyid": one.onlyid,
                "name": one.name,
                "cardclass": one.cardclass,
                "cardnum": one.cardnum,
                "amount": int(one.amount),
                "account": one.account,
                "remark": one.remark,
                "is_freeze": one.is_freeze,
                "is_confirm": one.is_confirm,
                "is_lock": one.is_lock,
                "user_group": one.user_group,
                "lock_user": one.lock_user,
                "spare1": one.spare1,
                "date_group": one.date_group.strftime('%Y-%m-%d'),
            }
            list1.append(dict1)
        resData = rf().code(200)
        resData["data"] = list1
        resData["total"] = len(total)
        resData["sum"] = newSum
        return self.finish(resData)


    # 删除数据
    async def delete(self, *args, **kwargs):
        reqData = json.loads(self.request.body.decode("utf8"))

        for one in reqData['data']:
            await self.application.objects.execute(
                Records.delete().where((Records.id == one["id"]) & (Records.onlyid == one["onlyid"])))
        self.finish(rf().set(204, "删除成功"))

