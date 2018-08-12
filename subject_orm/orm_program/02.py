"""
our purpuse is design : Student which some Fields have been record,

s1 = Student(name='zs', age=99)  类属性 name age
实例属性 name = 'zs'. 类属性 name = Field() 

"""
from field import *


class Model(dict):

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

    @property
    def age(self):
        return 20

class Student(Model):

    name = StringField(name="name")



if __name__ == '__main__':
    s = Student(name='zs')
    print(s.name)
    print(Model.__dict__)
    # print(s.name) s.name __dict__ 属性 Descriptor non-data, 处理掉 类属性, metaclass
