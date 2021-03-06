# -*- coding:utf-8 -*-
from tornado.web import URLSpec

from apps.system.handlers import (MenuHandler,MenuListHandler,PermissionHandler,PermissionMenuHandler,
                                  RolePermissionHandler,RoleHandler,UserRoleHandler,UserHandler,WhiteListHandler,
                                  WhiteListSetHandler)

urlpatterns = [
    URLSpec("/menu/", MenuHandler),
    URLSpec("/menu/list/", MenuListHandler),
    URLSpec("/menu/(\d+)/(\d+)/", MenuHandler),
    URLSpec("/permission/", PermissionHandler),
    URLSpec("/permission/menu/", PermissionMenuHandler),
    URLSpec("/permission/(\d+)/(\d+)/", PermissionHandler),
    URLSpec("/role/", RoleHandler),
    URLSpec("/role/permission/", RolePermissionHandler),
    URLSpec("/role/(\d+)/(\d+)/", RoleHandler),
    URLSpec("/user/", UserHandler),
    URLSpec("/user/(\d+)/(\d+)/", UserHandler),
    URLSpec("/user/role/", UserRoleHandler),
    URLSpec("/whitelist/", WhiteListHandler),
    URLSpec("/whitelist/set/", WhiteListSetHandler),
    URLSpec("/whitelist/(\d+)/(\d+)/", WhiteListHandler),
]
