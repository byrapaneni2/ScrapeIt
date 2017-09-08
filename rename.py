import sys
import re
import pickle
import os
import shutil

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
cities = load_obj('cities')
mta = []
bfa = []
sta = []
vil = []
pg = []
ph = []
rh = []
for city in cities:
	file = "obj/city_urls_rent/%s.txt" % city
	c=0
	with open(file,'r') as f:
		data = f.readlines()
	for i in data:
		if "Multistorey-Apartment" in i:
			mta.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue
		elif "Builder-Floor-Apartment" in i:
			bfa.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue

		elif "Studio-Apartment" in i:
			sta.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue

		elif "Residential-House" in i:
			rh.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue

		elif "Penthouse" in i:
			ph.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue

		elif "Villa" in i:
			vil.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue

		elif "Paying-Guest" in i or "Hostel-FOR-Rent" in i:
			pg.append(i[i.index("id=")+len("id="):].strip('\n'))
			continue

		else:
			c=c+1

	print city,c
	print len(mta)+len(bfa)+len(sta)+len(vil)+len(pg)+len(ph)+len(rh)
	print len(mta)

	#for root, dirs, files in os.walk('html/rent_html/apartment/%s/' %city):
	source = 'html/rent_html/apartment/%s/' %city
	dest1 = 'html/rent_html/multistorey-apartment/%s/' %city
	dest2 = 'html/rent_html/builderfloor-apartment/%s/' %city
	dest3 = 'html/rent_html/studio-apartment/%s/' %city
	files = os.listdir(source)
	for file in files:
		file = re.sub('%0A','',file)

		if file in mta:
			try:
				if not os.path.exists('html/rent_html/multistorey-apartment/'+city):
					os.makedirs('html/rent_html/multistorey-apartment/'+city)
				shutil.move(source+file+'%0A',dest1)	
				continue
			except IOError:
				pass
		elif file in bfa:
			try:
				if not os.path.exists('html/rent_html/builderfloor-apartment/'+city):
					os.makedirs('html/rent_html/builderfloor-apartment/'+city)
				shutil.move(source+file+'%0A',dest2)
				continue
			except IOError:
				pass
		elif file in sta:
			try:
				if not os.path.exists('html/rent_html/studio-apartment/'+city):
					os.makedirs('html/rent_html/studio-apartment/'+city)
				shutil.move(source+file+'%0A',dest3)
				continue
			except IOError:
				pass
		"""elif file in vil:
			continue
		elif file in rh:
			shutil.move(source+file,'html/rent_html/residential-house/%s/' %city)
		elif file in ph:
			shutil.move(source+file,'html/rent_html/residential-house/%s/' %city)
		elif file in pg:
			continue"""
			