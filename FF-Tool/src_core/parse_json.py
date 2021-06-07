import json
import sys
from pprint import pprint

with open('test.json') as data_file:    
    data = json.load(data_file)
pprint(data)

#______________________JSON__________________________
data = {"(1,2,3)":"('a','b','c')","(2,6,3)":"(6,3,2)"}
#with open('test1.json') as data_file:    
#    data = json.load(data_file)

json.dumps({str(k): v for k, v in data.items()})
pprint(data)
print(json.dumps(data))
#______________________JSON___________________________
d = {}
d[(5,7)] = ['five', 'seven']
json.dumps({str(k): v for k, v in d.items()})
pprint(d)
