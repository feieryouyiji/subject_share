class MetaClass(type):
    def __new__(MetaClass, name, bases, attrs):
        print(MetaClass, name, bases, attrs)

class Per():
  # __metaclass__ = MetaClass

  n = 'Per clas'

print(Per.n, 'Per<==')