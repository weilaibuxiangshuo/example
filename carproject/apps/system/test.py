import asyncio,time

async def ceshi():
    print("开始")
    await asyncio.sleep(2)
    print("结束")


async def main():
    print("11")
    start = time.time()
    list1 = []
    for i in range(3):
        await asyncio.gather(ceshi())
        # list1.append(asyncio.ensure_future(ceshi()))
    # await asyncio.wait(list1)
    await asyncio.gather(*list1)
    print("22",time.time()-start)


if __name__=="__main__":
    pass
    # loop = asyncio.get_event_loop()
    # asyncio.ensure_future(main())
    # loop.run_forever()
    # from collections import deque
    # b = deque()
    # b.append(1)
    # b.append(2)
    # print(b)
    # c = b.popleft()
    # print(c)
    # import hashlib
    # ss = hashlib.sha256("111111".encode('utf8'))
    # print(ss.hexdigest())
    # bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a