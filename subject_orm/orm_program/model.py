from orm import Model
from field import IntegerField, StringField


class Student(Model):
    id = IntegerField(is_primary_key=True)
    name = StringField()
    age = IntegerField()