import sys
import os
import pickle
import re
def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

cities = load_obj('cities')
c=0
for city in cities:
	file = 'obj/city_urls_sale/%s.txt' %city
	try:
		with open(file,'r') as f:
			data = f.readlines()
			print file
			print(len(data))
			data1 = list(set(data))
			print(len(data1))

		with open(file,'w') as f1:
			pass

		with open(file,'a') as f2:
			for d in data1:
				f2.write(d)
	except:
		c=c+1
print c