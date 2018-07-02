# coding:utf-8
# copy from http://www.lyyyuna.com/2018/04/28/python-orm1/
# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
# https://www.fullstackpython.com/object-relational-mappers-orms.html (good)

# https://github.com/aio-libs/aiomysql/issues/59
# https://www.jianshu.com/p/b5e347b3a17c

# http://blog.51cto.com/szgb17/2062283 (async orm demo)
# http://www.luameows.wang/2018/03/09/%E5%88%9B%E7%AB%8BORM-%E5%BB%96%E9%9B%AA%E5%B3%B0python%E7%AC%94%E8%AE%B0/ (async orm demo)

"""
Python做了如下的操作：

Foo中有__metaclass__这个属性吗？如果是，Python会在内存中通过__metaclass__创建一个名字为Foo的类对象（我说的是类对象，请紧跟我的思路）。如果Python没有找到__metaclass__，它会继续在Bar（父类）中寻找__metaclass__属性，并尝试做和前面同样的操作。如果Python在任何父类中都找不到__metaclass__，它就会在模块层次中去寻找__metaclass__，并尝试做同样的操作。如果还是找不到__metaclass__,Python就会用内置的type来创建这个类对象。

现在的问题就是，你可以在__metaclass__中放置些什么代码呢？答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到type或者子类化type的东东都可以。
"""

"""
当用户定义一个class User(Model)时，Python解释器首先在当前类User的定义中查找metaclass，如果没有找到，就继续在父类Model中查找metaclass，找到了，就使用Model中定义的metaclass的ModelMetaclass来创建User类，也就是说，metaclass可以隐式地继承到子类，但子类自己却感觉不到。

在ModelMetaclass中，一共做了几件事情：

排除掉对Model类的修改；

在当前类（比如User）中查找定义的类的所有属性，如果找到一个Field属性，就把它保存到一个__mappings__的dict中，同时从类属性中删除该Field属性，否则，容易造成运行时错误（实例的属性会遮盖类的同名属性）；

把表名保存到__table__中，这里简化为表名默认为类名。

在Model类中，就可以定义各种操作数据库的方法，比如save()，delete()，find()，update等等。



"""

from field import *

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        print(attrs, 'attrs<==')

        tablename = attrs.get('__table__', None) or name
        print 'Get table name', tablename
        mappings = {}
        fields = []
        primary = None
        for k, v in attrs.iteritems():   # name(k) = Field('ffl')(v) age = IntField(32)
            if isinstance(v, Field):
                print 'Found one field', k, v
                mappings[k] = v
                if v.primaryKey == True:
                    if primary == None:
                        primary = k
                    else:
                        raise RuntimeError("Duplicate primary key: %s", k)
                else:
                    fields.append(k)
        if primary == None:
            raise RuntimeError("No primary key given.")
        print('mapping.keys start---->>>', attrs)
        print('mapping', mappings)
        print('attrs', attrs)
        for k in mappings.keys():   #attrs 必须 删除 类属性,
            attrs.pop(k)              #如果 User 类属性 不删除的话 u.name 会直接访问类属性, 而不是实例属性, 其实就是model 中的字典 
        escaped_fields = list(map(lambda x: "'%s'" % x, fields))

        print('escaped_fields==>', escaped_fields)
        # renew attrs

        attrs['__mappings__'] = mappings 
        attrs['__table__'] = tablename
        attrs['__primarykey__'] = primary 
        attrs['__fields__'] = fields 
        # some basic sql commands
        attrs['__select__'] = "select '%s', %s from '%s'" % (primary, ','.join(escaped_fields), tablename)
        attrs['__insert__'] = "insert into '%s' (%s, '%s') values (%s)" % (tablename, ','.join(escaped_fields), primary, create_args_string(len(escaped_fields)+1))
        attrs['__update__'] = "update '%s' set %s where '%s' =?" % (tablename, ','.join(map(lambda x: "'%s'=?" % (mappings.get(x).name), fields)), primary)
        attrs['__delete__'] = "delete from '%s' where '%s' = ?" % (tablename, primary)

        print('new end attrs', attrs)
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMeta
    __table__ = 'Should not show'

    def __init__(self, **kw):
        print('enter model init')
        print(self, kw)
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            print('enter __getattr__', key)
            return self[key]
        except:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def select(cls, id):
        print "%s where '%s' = %s;" % (cls.__select__, cls.__primarykey__, id)

    def getValue(self, k):
        value = getattr(self, k, None)
        if value is None:
            field = self.__mappings__[k]
            if field.default is not None:
                value = field.default
                setattr(self, k, value)
        return value

    def save(self):
        args = map(self.getValue, self.__fields__)
        args.append(self.getValue(self.__primarykey__))
        print self.__insert__, args


class User(Model):
    __table__ = 'User_table'
    student_id = IntegerField('studentid', primaryKey=True)
    name = StringField('username')
    age = IntegerField('age')

    def shilifun(self,arg):
        print('shilifun ' + arg)
    
    @classmethod
    def clsfun(cls, arg):
        print("cls" + arg)

print 'Test relation fields Auto Finding:---------'
u = User()
print('u--->', u)

print 'Test select sql command:'
User.select(id=1)


print 'Test insert sql command:'
u2 = User(student_id=3, name='blue', age=123)
u2.save()

print('-------分割线-------')

print(u2.shilifun('gag'))
print(u2.clsfun('gag'))
print('this is will happen mircal')
print(u2.name)
print('this is will happen mircal')

print(u2['name'])
print(u2.__dict__)

print('User ', dir(User))
