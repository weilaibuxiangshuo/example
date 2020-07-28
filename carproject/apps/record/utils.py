# -*- coding:utf-8 -*-

from apps.record.models import Records
from tools.resful_api import Resf as rf


class RedisGroup:
    def __init__(self, obj):
        self.obj = obj
        self.rds = None
        self.only_id = None

    async def set(self, req):
        # print(self.obj)
        # print(self.obj.application)
        # 判断redis是否有记录
        self.only_id = req["onlyid"]

        # 实例化redis
        try:
            self.rds = self.obj.application.rds(1)
        except Exception as ff:
            return rf().set(500, "内部服务错误")

        # 判断标记是否存在
        if not self.rds.get("onlyid-mark"):
            self.rds.flushdb()
            self.rds.set("onlyid-mark", "1", ex=3600)
            allLockFreeze = await self.obj.application.objects.execute(Records.select().where(
                ((Records.is_freeze == True) | (Records.is_lock == True)) & (Records.is_confirm == False)))
            for oneLockFreeze in allLockFreeze:
                self.rds.set(oneLockFreeze.onlyid, oneLockFreeze.lock_user, ex=4800)

        # 判断是否存在redis里
        if not self.rds.get(self.only_id):
            self.rds.set(self.only_id, self.obj.current_user, ex=4800)
        else:
            getRdsVal = self.rds.get(self.only_id).decode('utf8')
            # 判断是否是相同用户操作
            if not getRdsVal == self.obj.current_user:
                return rf().set(404, "其它用户已锁定")

        return None

    async def get(self, req):
        # print(self.obj)
        # print(self.obj.application)
        # 判断redis是否有记录
        self.only_id = req["onlyid"]

        # 实例化redis
        try:
            self.rds = self.obj.application.rds(1)
        except Exception as ff:
            return rf().set(500, "内部服务错误")

        # 判断标记是否存在
        if not self.rds.get("onlyid-mark"):
            self.rds.flushdb()
            self.rds.set("onlyid-mark", "1", ex=3600)
            allLockFreeze = await self.obj.application.objects.execute(Records.select().where(
                ((Records.is_freeze == True) | (Records.is_lock == True)) & (Records.is_confirm == False)))
            for oneLockFreeze in allLockFreeze:
                self.rds.set(oneLockFreeze.onlyid, oneLockFreeze.lock_user, ex=4800)

        # 判断是否存在redis里
        if not self.rds.get(self.only_id):
            return rf().code(401)
        else:
            getRdsVal = self.rds.get(self.only_id).decode('utf8')
            # 判断是否是相同用户操作
            if not getRdsVal == self.obj.current_user:
                return rf().set(404, "其它用户已锁定")

        return None

    def delete(self):
        self.rds.delete(self.only_id)
