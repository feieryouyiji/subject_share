from field import *
from db import create_table, execute, select


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


class ModelMetaClass(type):

    def __new__(cls, future_class_name, future_class_parents, future_class_attrs):
        if future_class_name == 'Model':
            return type.__new__(cls, future_class_name, future_class_parents, future_class_attrs)


        mappings = {}  # 存储 表字段信息 tartget  找到 字段 信息 以及主键
        fields = []
        primary_key = None

        tablename = future_class_attrs.get('__table__', None) or future_class_name  # 在 表 类中写__table__ 属性
        for k, v in future_class_attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.is_primary_key:
                    if not primary_key:
                        primary_key = k
                    else:
                        raise RuntimeError("Duplicate primary key: %s", k)
                else:
                    fields.append(k)

        if not primary_key:
            raise RuntimeError("there is no primary key")

        # 如果不把类属性 上与实例 同名属性删除 , s.age 访问的永远是 类属性, 其实就是 Field 实例
        for key in mappings.keys():
            future_class_attrs.pop(key)

        # 如果不把 fields 再包 一层 字符串 的话, 构造 sql 的 时候 就 不会有引号 "select 'student_id', 'name','age' from 'User_table'"
        # escaped_fields = list(map(lambda f: r"%s" % f, fields))
        escaped_fields = fields

        # 重新 构造 类 新 的属性
        future_class_attrs['__mappings__'] = mappings
        future_class_attrs['__table__'] = tablename
        future_class_attrs['__primary_key__'] = primary_key
        future_class_attrs['__fields__'] = fields


        # 构造 CURD sql 语句
        future_class_attrs['__select__'] = "select %s,%s from %s" % (primary_key, ','.join(escaped_fields), tablename)
        future_class_attrs['__insert__'] = "insert into %s (%s, %s) VALUES (%s)" % (tablename, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields)+1))
        future_class_attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tablename, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        future_class_attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tablename, primary_key)

        return type.__new__(cls, future_class_name, future_class_parents, future_class_attrs)


class Model(dict, metaclass=ModelMetaClass):

    def __init__(self, **kw):  # 关键字传参, 只能用字典来接收 kw 里面 的 值
        print('enter model init')
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            print('enter __getattr__', key)
            return self[key]
        except:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


    def getValue(self, key):
        return getattr(self,key,None)

    def getValueOrDefault(self, key):
        value = getattr(self,key,None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                print('using default value for %s: %s'%(key,str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def find(cls, prikey):
        sql = '%s where %s = ?' % (cls.__select__, cls.__primary_key__)
        rs = await select(sql, [prikey], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])


    @classmethod
    async def find_all(cls, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy',None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?,?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s'%str(limit))
        rs = await select(' '.join(sql),args)
        return [cls(**r) for r in rs]



    async def save(self):
        try:
            args = list(map(self.getValueOrDefault, self.__fields__))
            args.append(self.getValueOrDefault(self.__primary_key__))
            print(args)
            print(self.__insert__)
            rows = await execute(self.__insert__, args)
            if rows != 1:
                print('failed to insert record: affect rows: %s' % rows)
        except BaseException as e:
            raise e
        print('save success')

    async def update(self):
        args = list(map(self.getValueOrDefault, self.__field__))
        args.append(self.getValue(self.__primary_key__))
        try:
            rows = await execute(self.__update__, args)
            if rows != 1:
                print('failed to update record: affect rows:%s' % rows)
        except BaseException as e:
            raise e


    async def remove(self):
        args = self.getValue(self.__primary_key__)
        rows = await execute(self.__delete__, args)
        if rows != 1:
            print('failed to remove record by primary key: affect rows:%s' % rows)


    @classmethod
    async def create_self(cls):
        try:
            columns = []
            for k, v in cls.__mappings__.items():
                columns.append('`%s` %s %s'%(k, v.sql_type, v.is_null))
                print('create_self columns', columns)
            print('cls=>',cls)
            columns.append('primary key (`%s`)' % cls.__primary_key__)
            sql = 'create table %s (%s) engine=innodb default charset=utf8' % (cls.__table__, ','.join(columns))
            await create_table(sql)
        except BaseException as e:
            raise e
