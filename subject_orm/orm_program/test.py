import aiomysql, asyncio

from db import *
from config import db_config
from model import Student


async def test_find_all():

    # 这里给的关键字参数按照xxx='xxx'的形式给出，会自动分装成dict
    rs = await Student.find_all(name='zs')		# rs是一个元素为dict的list
    # pdb.set_trace()
    for i in range(len(rs)):
        print(rs[i])


async def test_find():

    # 这里给的关键字参数按照xxx='xxx'的形式给出，会自动分装成dict
    rs = await Student.find(1)		# rs是一个元素为dict的list
    print('rs', rs)


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
        # s1 = Student(id=9, name="no yinhao", age=10)
        # await s1.save()

        # 查
        await test_find_all()
        # await test_find()

    except BaseException as e:
        print('create table is failed! error message:%s' % (e.args[0]))

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop=loop))
