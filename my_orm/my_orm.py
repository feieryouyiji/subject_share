# noqa
from my_field import *

## 我们需要 的是 对象.属性, 同时 对象[属性]
# 访问 u2.name 便等价于 u2[name]，而 User 间接继承自字典，User(student_id=3, name='blue', age=123)初始化后，便能访问字典元素u2[name]。 
# __setattr__ 是设置 key  eg: m.age= 21 , 会触发这个函数,但是 在这个函 数中继续 调用 m.age 会形成死循环, 可以使用 super.__setattr__

# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python/6581949#6581949
class ModelMetaClass(type):

    def __new__(cls, future_class_name, future_class_parents, future_class_attrs):
        print('cls', cls)
        print('name', future_class_name)
        print('bases', future_class_parents)
        print('----------')
        print('attrs', future_class_attrs)
        print('----------')
        # if future_class_name == 'Model':
        return type.__new__(cls, future_class_name, future_class_parents, future_class_attrs)

class Model(object, metaclass=ModelMetaClass):

    """
        实例属性在此init
    """
    # def __new__(cls, *args, **kwargs):
    #     return super().__new__(cls, *args, **kwargs)
        

    def __init__(self, **kwargs):
        print('enter __init', kwargs)
        super(Model, self).__init__(**kwargs)
        # self.name = kwargs['name']

    def __getattr__(self, key):
        try:
            print('enter __getattr__')
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        print('enter setattr', key, value)
        self[key] = value


class My(Model):

    name = StringField("name")


my = My(name="test")
print('my==>', my)
print('my==>', my.name)
print('======')
print('my', my.__dict__)
print('My', My.__dict__)
print('Model', Model.__dict__)


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
