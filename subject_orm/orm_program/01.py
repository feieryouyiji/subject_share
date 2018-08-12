"""
our purpuse is design : Student which some Fields have been record,

s1 = Student(name='zs', age=99)  类属性 name age , // 每一个学生都有 ? 实例 属性不行吗
实例属性 name = 'ffl'. 类属性 name = Field()

"""
class Student(Model):
    age = IntegerField()
    name = StringField()

s = Student(name='zs')
