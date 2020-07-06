# -*- coding:utf-8 -*-
import jwt
from datetime import datetime,timedelta

from tools.resful_api import Resf as rf

class JwtApi:
    def __init__(self):
        self.key = "ue_g&-4t2lhrd3+biy%1ujy0dsa8ayo6iq(@+&rup3#w==*)vxas8"
        #设置过期时间30秒
        self.expTime = datetime.utcnow()+timedelta(days=1)

    def encode(self,data):
        newData = {"exp":self.expTime}
        if isinstance(data,dict):
            newData.update(data)
        else:
            newData.update({"data":data})
        res = jwt.encode(newData,self.key)
        return res.decode("utf8")


    def decode(self,jwtToken):
        try:
            res = jwt.decode(jwtToken, self.key, algorithms=['HS256'])
            return res
        except jwt.exceptions.ExpiredSignatureError as e:
            return rf.code(401)
        except Exception as f:
            return rf.code(400)

if __name__=="__main__":
    temp = JwtApi()
    print(temp.decode("123123"))