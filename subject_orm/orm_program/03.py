"""
our purpuse is design : Student which some Fields have been record,

s1 = Student(name='zs', age=99)  类属性 name age , // 每一个学生都有 ? 实例 属性不行吗
实例属性 name = 'ffl'. 类属性 name = Field() //关键字传参
https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python/6581949#6581949
"""
from field import *


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
        escaped_fields = list(map(lambda x: "'%s'" % x, fields))

        # 重新 构造 类 新 的属性
        future_class_attrs['__mappings__'] = mappings
        future_class_attrs['__table__'] = tablename
        future_class_attrs['__primarykey__'] = primary_key
        future_class_attrs['__fields__'] = fields


        # 构造 CURD sql 语句
        future_class_attrs['__select__'] = "select `%s`, %s, from `%s`" % (primary_key, ','.join(escaped_fields), tablename)
        future_class_attrs['__insert__'] = "insert '%s', %s, from '%s'" % (primary_key, ','.join(escaped_fields), tablename)
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


class Student(Model):

    id = IntegerField(name='id', is_primary_key=True)

    name = StringField(name="name")

    



if __name__ == '__main__':
    s = Student(name='zs')
    # print(dir(Student))
    # print(Student.__class__)
    # print(Student.__class__ == Model.__class__)
    print('s.name==>', s.name)
    print('Student.__dict__', Student.__dict__)
    print('s.__dict__==>', s.__dict__)

