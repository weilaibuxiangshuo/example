# -*- coding:utf-8 -*-
from wtforms import StringField,ValidationError,FloatField,IntegerField
from wtforms.validators import data_required,length
from wtforms_tornado import Form
import re

class RecordsForm(Form):
    cardclass = StringField("所属银行")
    name = StringField("姓名")
    account = StringField("会员账号")
    amount = FloatField("金额")
    cardnum = StringField("银行卡号")

    def validate_cardclass(self,field):
        fd = field.data.strip()
        if len(fd)==0:
            raise ValidationError("所属银行不能为空")
        elif len(fd)<2 and len(fd)>128:
            raise ValidationError("所属银行长度在2到128个字符")
        pattern = re.compile(r"^[a-zA-Z\u4E00-\u9FA5\s]+$")
        reg = pattern.match(fd)
        if not reg:
            raise ValidationError("所属银行禁含有数字或非法字符")

    def validate_name(self,field):
        fd = field.data.strip()
        if len(fd)==0:
            raise ValidationError("姓名不能为空")
        elif len(fd)<2 and len(fd)>64:
            raise ValidationError("姓名长度在2到64个字符")
        pattern = re.compile(r"^[a-zA-Z\u4E00-\u9FA5\s]+$")
        reg = pattern.match(fd)
        if not reg:
            raise ValidationError("姓名禁含有数字或非法字符")

    def validate_account(self,field):
        fd = field.data.strip()
        if len(fd)==0:
            raise ValidationError("会员账号不能为空")
        pattern = re.compile(r"^[^\u4E00-\u9FA5\s]+$")
        reg = pattern.match(fd)
        if not reg:
            raise ValidationError("会员账号禁含有汉字或空格")

    def validate_amount(self,field):
        fd = str(int(field.data)).strip()
        if len(fd)==0:
            raise ValidationError("金额不能为空")
        pattern = re.compile(r"^[0-9]+$")
        reg = pattern.match(fd)
        if not reg:
            raise ValidationError("金额禁含有字母或负数或非法字符")
        if int(fd)>10000000:
            raise ValidationError("金额超过上限")

    def validate_cardnum(self,field):
        fd = field.data.strip()
        if len(fd)==0:
            raise ValidationError("银行卡号不能为空")
        elif len(fd)<16 or len(fd)>19:
            raise ValidationError("银行卡号位数16到19之间")
        pattern = re.compile(r"^[0-9]+$")
        reg = pattern.match(fd)
        if not reg:
            raise ValidationError("银行卡号禁含有字母或负数或非法字符")

