# -*- coding:utf-8 -*-
import peewee
from maincar.models import BaseModel

class Menus(BaseModel):
    title = peewee.CharField(max_length=32,verbose_name="菜单名")
    icon = peewee.CharField(max_length=32,verbose_name="图标")
    path = peewee.CharField(max_length=128,verbose_name="路径")
    code = peewee.CharField(max_length=32,verbose_name="编号")
    ord = peewee.IntegerField(verbose_name="序号",null=True)
    sub = peewee.ForeignKeyField("self", related_name="children", null=True, on_delete="CASCADE")

    @classmethod
    def newData(cls,params):
        params = tuple(params)
        if params:
            return cls.select().where(*params)
        else:
            return cls.select()


    class Meta:
        table_name="menus"


class Permissions(BaseModel):
    title = peewee.CharField(max_length=128,verbose_name="权限名")
    url = peewee.CharField(max_length=255,verbose_name="地址")
    method = peewee.CharField(max_length=30,verbose_name="请求方式")
    menu = peewee.ForeignKeyField(Menus,related_name="permiss_menu",null=True,on_delete="CASCADE")

    @classmethod
    def newData(cls,params):
        params = tuple(params)
        if params:
            return cls.select().where(*params)
        else:
            return cls.select()

    class Meta:
        table_name = "permissions"

class Roles(BaseModel):
    title = peewee.CharField(max_length=32,verbose_name="角色名")
    permission = peewee.ManyToManyField(Permissions, backref="role_permission",on_delete="CASCADE")

    @classmethod
    def newData(cls,params):
        params = tuple(params)
        if params:
            return cls.select().where(*params)
        else:
            return cls.select()

    class Meta:
        table_name="roles"

rolePermission = Roles.permission.get_through_model()


class Users(BaseModel):
    username = peewee.CharField(max_length=32,verbose_name="用户名")
    password = peewee.CharField(max_length=255,verbose_name="密码")
    is_staff = peewee.BooleanField(default=False,verbose_name="是否职员")
    is_superuser = peewee.BooleanField(default=False,verbose_name="是否管理员")
    is_lock = peewee.BooleanField(default=False,verbose_name="是否锁定")
    is_confirm = peewee.BooleanField(default=False,verbose_name="是否确定")
    role = peewee.ManyToManyField(Roles, backref="user_role",on_delete="CASCADE")

    @classmethod
    def newData(cls,params):
        params = tuple(params)
        if params:
            return cls.select().where(*params)
        else:
            return cls.select()

    class Meta:
        table_name = "users"



userRole = Users.role.get_through_model()


class WhiteList(BaseModel):
    ip = peewee.CharField(max_length=32,verbose_name="ip")
    is_through = peewee.BooleanField(default=False,verbose_name="是否通过")
    is_global = peewee.BooleanField(default=False,verbose_name="是否开启")

    @classmethod
    def newData(cls,params):
        params = tuple(params)
        if params:
            return cls.select().where(*params)
        else:
            return cls.select()

    class Meat:
        table_name = "whitelist"


