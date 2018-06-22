from dataclasses import dataclass

@dataclass
class SimpleDataObject(object):
  '''
  In this case,
  __init__, __repr__, __eq__,  will all be generated automatically.
  '''
  
  field_a: int
  field_b: str

example = SimpleDataObject(1, 'b')
print(example)  # SimpleDataObject(field_a=1, field_b='b')

example2 = SimpleDataObject(1, 'b')
print(example == example2)  # True