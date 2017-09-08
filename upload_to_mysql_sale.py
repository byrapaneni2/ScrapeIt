import peewee
from peewee import *
import MySQLdb
import pickle
import os
import json
import Geohash

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name +'.pkl', 'rb') as f:
        return pickle.load(f)

def load_obj1(name ):
    with open(name, 'rb') as f:
        return pickle.load(f)

db = MySQLDatabase('magicbricks_sale', user='root',passwd='@varsha')

class BaseModel(Model):
    class Meta:
        database = db

class Apartment(BaseModel):
    prop_id = peewee.IntegerField(unique=True,null=False)
    property_url = peewee.CharField(null=True)
    listed_by = peewee.CharField(null=True)
    property_type =peewee.CharField(null=True)
    posted_date = peewee.DateTimeField(null=True)
    name = peewee.CharField(null=True)
    city = peewee.CharField(null=True)
    locality = peewee.CharField(null=True)
    address = peewee.CharField(null=True)
    landmark = peewee.CharField(null=True)
    covered_area = peewee.IntegerField(null=True)
    carpet_area = peewee.IntegerField(null=True)
    price = peewee.IntegerField(null=True)
    latitude = peewee.CharField(null=True)
    longitude = peewee.CharField(null=True)
    geo_hash = peewee.CharField(null=True)
    bhk = peewee.IntegerField(null=True)
    bedroom_dimensions = peewee.CharField(null=True)
    bathrooms = peewee.IntegerField(null=True)
    balcony = peewee.IntegerField(null=True)
    furnished_status = peewee.CharField(null=True)
    floor_num = peewee.CharField(null=True)
    age_of_construction = peewee.CharField(null=True)
    status = peewee.CharField(null=True)
    posession_by = peewee.CharField(null=True)
    transaction_type = peewee.CharField(null=True)
    type_of_ownership = peewee.CharField(null=True)
    owner_name = peewee.CharField(null=True)
    agent_name = peewee.CharField(null=True)
    agent_url = peewee.CharField(null=True)
    agent_operation_year = peewee.CharField(null=True)
    agent_address = peewee.CharField(null=True)
    agent_dealing_in = peewee.CharField(null=True)
    agent_prop_url = peewee.CharField(null=True)
    agent_prop_count = peewee.CharField(null=True)
    project_name = peewee.CharField(null=True)
    developer_name = peewee.CharField(null=True)
    project_url = peewee.CharField(null=True)
    flooring = peewee.CharField(null=True)
    electricity_availability = peewee.CharField(null=True)
    water_availability = peewee.CharField(null=True)
    facing = peewee.CharField(null=True)
    car_parking = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    file_id = peewee.CharField(unique=True,null=False)

db.connect()
db.create_tables([Apartment], safe=True)

properties_sale_apartment = []
ctr = 0
#cities = load_obj('cities')
cities = ['Agra']
c=0
for city in cities:
    root = 'parsed/sale/apartment/%s' %city
    try:
        for file in os.listdir(root):
            if os.path.isfile(file):
                continue

            if file.endswith(".pkl"):
                ctr += 1
                path = '%s/%s' % (root, file)
                Property = load_obj1(path)
                properties_sale_apartment.append(Property['prop_details'])      
            if ctr%5000 == 0:
                print ctr
    except OSError:
        c=c+1
print c
save_obj(properties_sale_apartment, 'properties_sale_apartment')

left = 0
properties = []
properties = load_obj1('obj/properties_sale_apartment.pkl')
with db.atomic():
    num = 1
    for idx in range(0, len(properties), num):
        if idx%1000 == 0:
            print idx
        try:
            d = properties[idx]
            Apartment.create(**d)
        except:
            left = left+1
print left
db.close()