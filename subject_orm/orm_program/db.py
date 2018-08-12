import aiomysql, asyncio

print('aiomysql', aiomysql)
async def create_pool(loop, **kw):
    print('create database connect pool..... ')
    global  __pool
    __pool = await aiomysql.create_pool(
        minsize = kw.get('minsize', 1),
        maxsize = kw.get('maxsize', 10),
        loop = loop,
        host = kw.get('host','localhost'),
        port = kw.get('port', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset','utf8'),
        autocommit = kw.get('autocommit',True)
    )


async def create_db(name):
    global __pool
    with (await __pool) as conn:
        try:
            cursor = await conn.cursor()
            await cursor.execute('drop database if exists '+name)
            await cursor.execute('create database '+name)
        except BaseException as e:
            await conn.rollback()
            print('create database failed, mysql error:%d:%s'%(e.args[0],e.args[1]))
        finally:
            cursor.close()


async def drop_db(host, user, pw=None, name=None):
    global __pool
    with (await __pool) as conn:
        try:
            cursor = await conn.cursor()
            await cursor.execute('drop database if exists '+name)
        except BaseException as e:
            print('create database failed, mysql error:%d:%s'%(e.args[0],e.args[1]))
        finally:
            cursor.close()
            

async def create_table(sql):
    global __pool                
    with (await __pool) as conn:
        try:
            cursor = await conn.cursor()
            ret = await cursor.execute(sql)
            if ret is not None:
                print('executed succ')
            else:
                print('executed failed')
        except aiomysql.Error as e:
            raise e
        finally:
            await cursor.close()


async def select(sql, args, size=None):
    log(sql,args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('row return count:%s'%len(rs))
        return rs


async def execute(sql, args, autocommit=True):
    log(sql)
    global __pool
    with (await __pool) as conn:
        if not autocommit:
            await conn.begin()
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affect = cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise e
        return affect