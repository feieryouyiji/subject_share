
# class T(dict):
#   pass

# t = T(a='a')
# print(t.__dict__)
# print(t['a'])


# class A():
#   name = 'A'
  
#   def __init__(self, name):
#       self.name = name 

# class B(A):
#   name = 'B'

# b = B(name="b instance")


class My(dict):

    def __init__(self, *args, **kw):
        super().__init__(self, *args, **kw)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

class T(My):
    # name = "T name"
    pass

t = T(name="test name")
print(t.name)
print(dir(t))
print(t.__dict__)