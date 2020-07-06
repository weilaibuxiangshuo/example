# -*- coding:utf-8 -*-

async def deepRes(*args,**kwargs):
    self,data,num,dataList,*other = args
    resList = []
    num += 1
    for one in data:
        resDict = {}
        res = await self.application.objects.execute(one.children)
        if not len(res) == 0:
            resDict['children'] = await deepRes(self, one.children,num,dataList)
            if not resDict['children']:
                continue
        else:
            #匹配符合权限，不符合跳出循环，不添加
            isBool = False
            for two in dataList:
                if two['id'] == one.id and two['title'] == one.title:
                    isBool = True
                    resDict['children'] = two['children']
                    for three in resDict['children']:
                        three['level'] = num + 1
            if not isBool:
                continue
        resDict['id']=one.id
        resDict['title']=one.title
        resDict['level']=num
        resList.append(resDict)
    return resList




