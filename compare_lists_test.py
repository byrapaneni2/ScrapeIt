import sys

file1 = "obj/city_urls_rent/Mumbai.txt"
file2 = "obj/city_urls_sale/Mumbai.txt"
with open(file1,'r') as f:
	data1 = f.readlines()
data1 = [data[data.index("id=")+len("id="):] for data in data1]
data1 = list(set(data1))
data1 = data1.append("4d423237353635353131")
print data1[10]

with open (file2,'r') as f:
	data2 = f.readlines()
data2 = [data[data.index("id=") + len("id="):] for data in data2]
data2 = list(set(data2))
print data2[0]

l = [i for i in data1 if i  in data2]
print len(l)