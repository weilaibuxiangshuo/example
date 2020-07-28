# -*- coding:utf-8 -*-
from functools import update_wrapper, wraps

def dispatch_methods(multi):
    #判断参数是否为列表，不是列表转为列表
    if not isinstance(multi, list):
        multi = [multi]

    def wrapper_entry(cls):
        #判断是否是类
        if isinstance(cls,type):
            #获取cls里面已定义的请求
            methodList = [m for m in [getattr(cls, i) for i in ["get", "post", "put", "delete"] if hasattr(cls, i)] if
                          m.__name__ in ["get", "post", "put", "delete"]]
            async def _wrapper(self, *args, **kwargs):
                #根据request请求获取对应的方法
                newMethod = [method for method in methodList if method.__name__ == self.request.method.lower()][0]
                # 封装所有装饰器
                for dec in multi:
                    newMethod = dec(newMethod)
                return  await newMethod(self, *args, **kwargs)
            #设置如请求在列表中，则执行_wrapper函数
            for s in ["get", "post", "put", "delete"]:
                setattr(cls, s, _wrapper)
            return cls
        else:
            #函数执行如下
            async def _wrapper_func(self,*args,**kwargs):
                return await cls(self,*args,**kwargs)
            for dec in multi:
                _wrapper_func = dec(_wrapper_func)
            update_wrapper(_wrapper_func,cls)
            return _wrapper_func
    return wrapper_entry

if __name__ == "__main__":
    pass
