# noqa
from my_field import *

## 我们需要 的是 对象.属性, 同时 对象[属性]
# 访问 u2.name 便等价于 u2[name]，而 User 间接继承自字典，User(student_id=3, name='blue', age=123)初始化后，便能访问字典元素u2[name]。 
# __setattr__ 是设置 key  eg: m.age= 21 , 会触发这个函数,但是 在这个函 数中继续 调用 m.age 会形成死循环, 可以使用 super.__setattr__

# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python/6581949#6581949


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

        if not primary_key:
            raise RuntimeError("there is no primary key")

        # 如果不把类属性 上与实例 同名属性删除 , s.age 访问的永远是 类属性, 其实就是 Field 实例
        for key in mappings.keys():
            future_class_attrs.pop(key)

        # 如果不把 fields 再包 一层 字符串 的话, 构造 sql 的 时候 就 不会有引号 "select 'student_id', 'name','age' from 'User_table'"
        escaped_fields = list(map(lambda x: "'%s'" % x, fields))

        # 重新 构造 类 新 的属性
        future_class_attrs['__mappings__'] = mappings
        future_class_attrs['__table__'] = tablename
        future_class_attrs['__primarykey__'] = primary_key
        future_class_attrs['__fields__'] = fields

        # 构造 CURD sql 语句
        future_class_attrs['__select__'] = "select '%s', %s, from '%s'" % (primary_key, ','.join(escaped_fields), tablename)
        future_class_attrs['__insert__'] = "insert '%s', %s, from '%s'" % (primary_key, ','.join(escaped_fields), tablename)
        # attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        # 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))


class Model(dict, metaclass=ModelMetaClass):

    """
        继承 dict 的目的是为了方便 像字典一样 存取 属性值
    """
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            print('enter __getattr__')
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class Student(Model):

    __table__ = 'student'

    name = StringField()
    age = IntegerField(is_primary_key=True)

##########
# class ModelMetaclass(type):

#     def __new__(cls, name, bases, attrs):
#         # 排除Model类本身:
#         if name=='Model':
#             return type.__new__(cls, name, bases, attrs)
#         # 获取table名称:
#         tableName = attrs.get('__table__', None) or name
#         logging.info('found model: %s (table: %s)' % (name, tableName))
#         # 获取所有的Field和主键名:
#         mappings = dict() # 
#         fields = []
#         primaryKey = None
#         for k, v in attrs.items():
#             if isinstance(v, Field):
#                 logging.info('  found mapping: %s ==> %s' % (k, v))
#                 mappings[k] = v
#                 if v.primary_key:
#                     # 找到主键:
#                     if primaryKey:
#                         raise RuntimeError('Duplicate primary key for field: %s' % k)
#                     primaryKey = k
#                 else:
#                     fields.append(k)
#         if not primaryKey:
#             raise RuntimeError('Primary key not found.')
#         for k in mappings.keys():
#             attrs.pop(k)   # 删除字段的类属性
#         escaped_fields = list(map(lambda f: '`%s`' % f, fields))
#         attrs['__mappings__'] = mappings # 保存属性和列的映射关系
#         attrs['__table__'] = tableName
#         attrs['__primary_key__'] = primaryKey # 主键属性名
#         attrs['__fields__'] = fields # 除主键外的属性名
#         # 构造默认的SELECT, INSERT, UPDATE和DELETE语句:
#         attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
#         attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
#         attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
#         attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
#         return type.__new__(cls, name, bases, attrs)

# 只是为了Model编写方便，放在元类里和放在Model里都可以
    # attrs['__select__']="select %s ,%s from %s " % (primaryKey,','.join(map(lambda f: '%s' % (mappings.get(f).name or f ),fields )),tableName)
    # attrs['__update__']="update %s set %s where %s=?"  % (tableName,', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)),primaryKey)
    # attrs['__insert__']="insert into %s (%s,%s) values (%s);" % (tableName,primaryKey,','.join(map(lambda f: '%s' % (mappings.get(f).name or f),fields)),create_args_string(len(fields)+1))
    # attrs['__delete__']="delete from %s where %s= ? ;" % (tableName,primaryKey)
