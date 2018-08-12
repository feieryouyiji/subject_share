import aiomysql, asyncio

from db import *
from config import db_config
from model import Student


async def init(loop):
    try:
        await create_pool(loop = loop, **db_config)
    except aiomysql.Error as e:
        print('create pool is failed! errno:%s '% str(e))
        return
    try:
        # 创建 表
        is_exist_db = await isExistTBL(db_config['db'], 'Student')
        if not is_exist_db:
            print('不存在')
            await Student.create_self()
        print('存在')
        s1 = Student(id=1, name="zs", age=10)
        await s1.save()
        #await blog.create_self()
        #await comment.create_self()
    except BaseException as e:
        print('create table is failed! error message:%s'%(e.args[0]))

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop = loop))