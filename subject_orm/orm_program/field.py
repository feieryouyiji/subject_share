
"""
  name: '',
  sqy_type: 'character varying(100) || integer',
  is_primary: Bool,
  default: '',
"""


class Field(object):
    def __init__(self, name, sql_type, is_primary_key, is_null, default):
        self.name = name
        self.sql_type = sql_type
        self.is_primary_key = is_primary_key
        self.is_null = is_null
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__, self.sql_type, self.name)


class IntegerField(Field):

    def __init__(self, name=None, sql_type='bigint',
                 is_primary_key=False, is_null='not null', default=''):
        super(IntegerField, self).__init__(name, sql_type, 
                                           is_primary_key,is_null, default)


class StringField(Field):

    def __init__(self, name=None, sql_type='varchar(100)',
                 is_primary_key=False, is_null='not null', default=''):
        super(StringField, self).__init__(name, sql_type, 
                                          is_primary_key,is_null, default)

