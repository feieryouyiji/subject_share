# coding:utf-8

# https://www.zhihu.com/question/20040039(super的讲解)
# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
# the metaclass will automatically get passed the same argument
# that you usually pass to `type`

"""
    因为 写在模块中的__meta__ 会把 这个模块所有的类 的metaclass 变成 upper_attr , 其实就是 type = upper_attr 两个不同的变量拥有同一个作用
"""
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    """
      Return a class object, with the list of its attribute turned
      into uppercase.
    """
    print(future_class_name, future_class_parents, future_class_attr, 'upper_attr ---')
    # pick up any attribute that doesn't start with '__' and uppercase it
    uppercase_attr = {}
    for name, val in future_class_attr.items():
        if not name.startswith('__'):
            uppercase_attr[name.upper()] = val
        else:
            uppercase_attr[name] = val

    # let `type` do the class creation
    return type(future_class_name, future_class_parents, uppercase_attr)

__metaclass__ = upper_attr # this will affect all classes in the module

class Foo(): # global __metaclass__ won't work with "object" though
    # but we can define __metaclass__ here instead to affect only this class
    # and this will work with "object" children
    bar = 'bip'
class Person():
    pass

print(hasattr(Foo, 'bar'))
# Out: False
print(hasattr(Foo, 'BAR'))
# Out: True

f = Foo()
print(f.BAR)
# Out: 'bip'
print(type == upper_attr)