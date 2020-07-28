# -*- coding:utf-8 -*-
import peewee
import datetime,uuid

from maincar.models import BaseModel

from maincar.mysqlconfig import asyncConnMysql

class Records(BaseModel):
    id = peewee.AutoField()
    onlyid = peewee.CharField(max_length=255,verbose_name="订单号")
    name = peewee.CharField(max_length=64,verbose_name="姓名")
    cardclass = peewee.CharField(max_length=128,verbose_name="卡类")
    cardnum = peewee.CharField(max_length=128,verbose_name='卡号')
    amount = peewee.DecimalField(verbose_name="金额",max_digits=10,decimal_places=0)
    date_group = peewee.DateTimeField(verbose_name="所属日期")
    user_group = peewee.CharField(max_length=32,verbose_name="所属用户")
    account = peewee.CharField(max_length=128,verbose_name="会员账号")
    operator = peewee.CharField(max_length=128,null=True,default=None,verbose_name="操作人")
    is_lock = peewee.BooleanField(default=False,verbose_name="是否锁定")
    is_freeze = peewee.BooleanField(default=False,verbose_name="是否冻结")
    is_confirm = peewee.BooleanField(default=False,verbose_name="是否确认")
    is_fail = peewee.BooleanField(default=False,verbose_name="是否失败")
    remark = peewee.TextField(null=True,default=None,verbose_name="备注")
    lock_user = peewee.CharField(max_length=32,null=True,default=None,verbose_name="锁定的用户")
    last_time = peewee.DateTimeField(default=None,null=True,verbose_name="最后一次修改时间")
    uuidnum = peewee.CharField(max_length=255,default=uuid.uuid1,verbose_name="标记")
    spare1 = peewee.CharField(max_length=128,verbose_name="备用1",null=True,default=None)
    spare2 = peewee.CharField(max_length=128,verbose_name="备用2",null=True,default=None)

    @classmethod
    def newdata(cls,params):
        params = tuple(params)
        if params:
            return cls.select().where(*params)
        else:
            return cls.select()

    class Meta:
        database = asyncConnMysql().database
        table_name = "records"


def initialze():
    asyncConnMysql().database.create_tables([Records])

if __name__=="__main__":
    initialze()

