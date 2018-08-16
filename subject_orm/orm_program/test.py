import aiomysql, asyncio

from db import *
from config import db_config
from model import Student


async def test_find_all():

    res = await Student.find_all(name='zs', limit=2)		# rs是一个元素为dict的list
    # pdb.set_trace()
    for i in range(len(res)):
        print(res[i])


async def test_find():

    res = await Student.find(1)
    print('res', res)

async def test_remove():
    res = await Student(id=1).remove()
    print('res', res)

async def test_update():
    res = await Student(id=1, name="update", age=22).update()
    print('res', res)

async def init(loop):
    try:
        await create_pool(loop = loop, **db_config)
    except aiomysql.Error as e:
        print('create pool is failed! errno:%s '% str(e))
        return
    try:
        # 创建 表
        # is_exist = await is_exist_table(db_config['db'], 'Student')
        # if not is_exist:
        #     await Student.create_self()
        # s1 = Student(id=1, name="no yinhao", age=10)
        # await s1.save()

        # 查
        # await test_find()

        # 删
        # await test_remove()

        # 改
        await test_update()

    except BaseException as e:
        print('error message:%s' % (e.args[0]))

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop=loop))
