# -*- coding:utf-8 -*-
from apps.system.models import Menus,Permissions,Roles,Users,rolePermission,userRole,WhiteList
from maincar.mysqlconfig import asyncConnMysql


def initialze():
    asyncConnMysql().database.create_tables([Menus,Permissions,Roles,Users,rolePermission,userRole,WhiteList])

if __name__=="__main__":
    initialze()