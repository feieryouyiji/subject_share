
"""
  name: '',
  sqy_type: 'character varying(100) || integer',
  is_primary: Bool,
  default: '',
"""


class Field(object):
    def __init__(self, name, sql_type, is_primary_key, default):
        self.name = name
        self.sql_type = sql_type
        self.is_primary_key = is_primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__, self.sql_type, self.name)


class IntegerField(Field):

    def __init__(self, name=None, sql_type='INTEGER',
                 is_primary_key=False, default=''):
        super(IntegerField, self).__init__(name, sql_type, 
                                           is_primary_key, default)


class StringField(Field):

    def __init__(self, name=None, sql_type='VARCHAR',
                 is_primary_key=False, default=''):
        super(StringField, self).__init__(name, sql_type, 
                                          is_primary_key, default)

