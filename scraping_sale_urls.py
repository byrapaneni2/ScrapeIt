import sys
import re
import pickle
import os
import re

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

cities = load_obj('cities')
for city in cities:
	try:
		file = "obj/city_urls_sale/%s.txt" % city
		c=0
		with open(file,'r') as f:
			data = f.readlines()
		for i in data:
			if "Apartment" in i:
				if not os.path.exists('obj/city_urls_sale/urls_sale_apartment'):
					os.mkdir('obj/city_urls_sale/urls_sale_apartment')
				with open('obj/city_urls_sale/urls_sale_apartment/%s.txt' %city,'a') as f:
					f.write(i)
				continue
			elif "Villa" in i:
				if not os.path.exists('obj/city_urls_sale/urls_sale_villa'):
					os.mkdir('obj/city_urls_sale/urls_sale_villa')
				with open('obj/city_urls_sale/urls_sale_villa/%s.txt' %city,'a') as f:
					f.write(i)
				continue
			elif "Residential-Plot" in i:
				if not os.path.exists('obj/city_urls_sale/urls_sale_plot'):
					os.mkdir('obj/city_urls_sale/urls_sale_plot')
				with open('obj/city_urls_sale/urls_sale_plot/%s.txt' %city,'a') as f:
					f.write(i)
				continue
			elif "Residential-House" in i or "Penthouse" in i:
				if not os.path.exists('obj/city_urls_sale/urls_sale_house'):
					os.mkdir('obj/city_urls_sale/urls_sale_house')
				with open('obj/city_urls_sale/urls_sale_house/%s.txt' %city,'a') as f:
					f.write(i)
				continue
			else:
				c=c+1
			print city,c
	except:
		print city,"Not Scraped"
	