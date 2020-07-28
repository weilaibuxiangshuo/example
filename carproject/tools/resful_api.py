# -*- coding:utf-8 -*-


class Resf(object):
    """
    200  服务器成功返回用户的请求数据
    201 create 用户创建或修改数据成功
    202 Accept有一个请求进入后台排队
    204 No Content 删除数据成功
    400 用户发送的请求有错误，服务器没有进行新建或修改操作
    401用户没有权限 用户名，密码错误
    403 用户得到授权，但是访问被禁止
    404 用户发出的请求是不存在的记录，服务器没有进行操作
    406用户请求的格式不对
    410 用户请求的资源被永久删除，不会被诶获得
    500 服务器错误，用户无法进行判断是否请求成功
    """

    def __init__(self):
        self.listCode = {
            200: {"code": 200, "msg": "请求成功"},
            201: {"code": 201, "msg": "创建成功"},
            202: {"code": 202, "msg": "更新成功"},
            204: {"code": 204, "msg": "删除成功"},
            400: {"code": 400, "msg": "信息有误"},
            401: {"code": 401, "msg": "用户没有权限"},
            403: {"code": 403, "msg": "此信息有误"},
            404: {"code": 404, "msg": "操作失败"},
        }


    def code(self, num):
        return self.listCode[num]

    def set(self, num, msg):
        res = {"code": num, "msg": msg}
        return res
