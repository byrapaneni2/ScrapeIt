import sys
import re
import pickle

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
cities = load_obj('cities')
for city in cities:
	file = "obj/city_urls_rent/%s.txt" % city
	c=0
	with open(file,'r') as f:
		data = f.readlines()
	for i in data:
		if "Apartment" in i: # urls with "Multistorey-Apartment" or "Builder-Floor-Apartment" or "Studio-Apartment" are stored in this folder
			with open('obj/city_urls_rent/urls_rent_apartment/%s.txt' %city,'a') as f:
				f.write(i)
			continue

		elif "Villa" in i: # urls with "Villa"
			with open('obj/city_urls_rent/urls_rent_villa/%s.txt' %city,'a') as f:
				f.write(i)
			continue

		elif "Residential-House" in i or "Penthouse" in i: # urls with "Residential-House" or "Penthouse"
			with open('obj/city_urls_rent/urls_rent_house/%s.txt' %city,'a') as f:
				f.write(i)
			continue

		elif "Paying-Guest" in i or "Hostel-FOR-Rent" in i: # urls with "Paying-Guest" or "Hostel-FOR-Rent"
			with open('obj/city_urls_rent/urls_rent_pg/%s.txt' %city,'a') as f:
				f.write(i)
			continue

		else:
			c=c+1
	print city,c