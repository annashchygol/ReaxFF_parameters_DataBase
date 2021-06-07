import yaml

document1 = """
  a: 1
  b:
    c: 3
    d: 4
"""
print( yaml.dump(yaml.load(document1)))

stream1 = open('test.yaml', 'r') 
obj = yaml.load(stream1)
print("Object, loaded from file:")
print(obj)
print(obj["KEY"]["bonds"])
#print(inspect.getmembers(obj))

#print(inspect.getmembers('OLOLO'))
stream2 = open('test2.yaml', 'w') 
yaml.dump(document1, stream2)
print (yaml.dump(document1))
