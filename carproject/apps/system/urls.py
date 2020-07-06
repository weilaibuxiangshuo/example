# -*- coding:utf-8 -*-
from tornado.web import URLSpec

from apps.system.handlers import (MenuHandler,MenuListHandler,PermissionHandler,PermissionMenuHandler,
                                  RolePermissionHandler,RoleHandler,UserRoleHandler,UserHandler)

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
    URLSpec("/user/role/", UserRoleHandler),
]
