# -*- coding:utf-8 -*-
from datetime import datetime,date
def json_serial(obj):
    if isinstance(obj,(datetime,date)):
        return obj.isoformat()
    raise TypeError("类型错误")

