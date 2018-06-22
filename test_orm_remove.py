
import pprint
pp = pprint.PrettyPrinter(indent=4)


entity_relation_map = {
  'waiter': {
    'fk': [
      {
        'db': 'shop',
        'field': 'shop',
      }
    ]
  },
  'service': {
    'fk': []
  },
  'work': {
    'fk': [
      {
        'db': 'waiter',
        'field': 'waiter',
      }
    ]
  },
  'waiter_service_relation': {
    'fk': [
      {
        'db': 'waiter',
        'field': 'waiter',
      },
      {
        'db': 'service',
        'field': 'service',
      }
    ]
  },
  'tag': {
    'fk': [],
  },
  'waiter_tag_relation': {
    'fk': [
      {
        'db': 'waiter',
        'field': 'waiter',
      },
      {
        'db': 'tag',
        'field': 'tag',
      }
    ]
  },
  'shop': {
    'fk': [
      {
        'db': 'category',
        'field': 'area',
      }
    ]
  },
  'category': {
    'fk': []
  }
}


class EntityRelationMap(object):

    def __init__(self, config, context):
        self.context = context
        self.relation_map = config
        self._init_relation()
        self.remove_count = 0

    def _init_relation(self):
        relation_map = self.relation_map
        self.dbname_list = list(relation_map.keys())
        for dbname in self.relation_map:
            # 给每一个 db_dict 加上 many_fk 空数组
            db_dict = self.relation_map[dbname]
            if db_dict.get('many_fk') is None:
                db_dict.update(many_fk=[])

            # 循环遍历所有fk, 指向谁就在那个db_dict.many_fk push 进去
            for fk_dict in db_dict['fk']:
                fk_dbname = fk_dict['db']
                fk_field = fk_dict['field']
                print(fk_dbname, fk_field)
                if self.relation_map[fk_dbname].get('many_fk') is None:
                    self.relation_map[fk_dbname].update(many_fk=[])
                self.relation_map[fk_dbname]['many_fk'].append({'db': dbname, 'field': fk_field })

    def _loop_remove(self, dbname):
        relation_map = self.relation_map
        many_fk_list = relation_map[dbname]['many_fk']
        if not many_fk_list:
            # 此dbname没有关联的谁指向它
            print('删除%s, 然后跳出了循环' % dbname)
            self.remove_count = self.remove_count + 1
            return 
        else:  # many_fk 指向它
            print('先删除dbname自己, 再删除ta的 many_fk', dbname)
            self.remove_count = self.remove_count + 1
            for many_fk_dict in many_fk_list:
                self._loop_remove(many_fk_dict['db'])

    def remove_item(self, item, dbname):
        print('开始删除---start')
        self._loop_remove(dbname)

        print('结束删除---end', self.remove_count)


context = 'context'

erm = EntityRelationMap(entity_relation_map, context)

print(erm, 'erm')
print(len(erm.dbname_list), 'erm')
pp.pprint(erm.relation_map)

print('----------------')

item = {}

erm.remove_item(item, 'category')

print('----------------')