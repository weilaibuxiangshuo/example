# -*- coding:utf-8 -*-
import json

from wtforms.fields import StringField,IntegerField
from wtforms.validators import length,data_required,StopValidation,ValidationError
from wtforms_tornado.form import Form

class MenusForm(Form):
    title = StringField('菜单名',validators=[data_required("菜单名不能为空"),length(min=3,max=32,message="长度在3到32位字符")])
    icon = StringField('图标',validators=[data_required("图标不能为空"),length(min=1,max=32,message="长度在1到32位字符")])
    path = StringField('地址',validators=[data_required("地址不能为空"),length(min=1,max=128,message="长度在1到128位字符")])
    code = StringField('编号',validators=[data_required("编号不能为空"),length(min=1,max=32,message="长度在1到32位字符")])
    ord = IntegerField('序号',validators=[data_required("序号不能为空")])


class PermissionsForm(Form):
    title = StringField('权限名',validators=[data_required("权限名不能为空"),length(min=3,max=128,message="长度在3到32位字符")])
    url = StringField('地址',validators=[data_required("地址不能为空"),length(min=1,max=255,message="长度在1到32位字符")])
    method = StringField('请求方式')
    menu = IntegerField('关联菜单',validators=[data_required("关联菜单不能为空")])
    def validate_method(self,field):
        temp = eval(field.data)
        if len(temp)==0:
            raise ValidationError(message="请求方式不能为空")


class RoleForm(Form):
    title = StringField('角色名',validators=[length(max=32,min=3,message="长度在3到32位字符"),data_required("角色名不能为空")])



class UserForm(Form):
    username = StringField('用户名',validators=[length(max=32,min=5,message="长度在5到32个字符"),data_required("角色名不能为空")])
    password = StringField('密码',validators=[length(min=6,message="长度至少6个字符或以上"),data_required("密码不能为空")])