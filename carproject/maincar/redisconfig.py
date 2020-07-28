# -*- coding:utf-8 -*-

import redis

class BaseRedis(redis.StrictRedis):
    def __init__(self,n=0):
        #判断1，用户2，普通0
        super(BaseRedis,self).__init__(db=n,host='localhost',port=6379)
