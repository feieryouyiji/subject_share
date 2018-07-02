
class Parent():

    name = 'Parent'
    def __init__(self, name):
        self.name = name

class Son(Parent):

    name = 'son'
    pass

s = Son(name="i am son")

print(s.name)