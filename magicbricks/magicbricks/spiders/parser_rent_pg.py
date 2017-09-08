import scrapy
import pickle
import os
import re
import json
import shutil
import Geohash

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

def price_to_decimal(price, price_unit):
    if price_unit == 'Lac' or price_unit =='L':
        return price*10**5
    elif price_unit == 'Crore' or price_unit =='Cr':
        return price*10**7

root = '/Users/varshathanooj/Documents/GitHub/Flatopedia/magicbricks'

class MagicBricks(scrapy.Spider):
    
    name = "parser_rent_pg"

    def start_requests(self):
        #cities = load_obj('cities')
        cities = ['Agra']
        for city in cities:
            if not os.path.exists('html/rent_html/pg/'+city):
                continue

            if not os.path.exists('parsed/rent/pg/'+city):
                os.makedirs('parsed/rent/pg/'+city)

            for file in os.listdir('html/rent_html/pg/'+city):
                file_id = file
                url = 'file://%s/html/rent_html/pg/%s/%s' % (root,city,file)

                yield scrapy.Request(url=url, callback=self.parse, meta={ 'city':city,'url':url, 'file_id':file_id})
               
    def parse(self, response):
        prop_details = {}
        Property = {}

        #Basic Details
        prop_id = response.xpath("//div[@class='propertyId']").extract()
        prop_id = re.findall(r'\b\d+\b',prop_id[0])
        prop_id = str(prop_id[0])
        property_url = response.xpath("//link[@rel='canonical']/@href").extract()
        listed_by = response.xpath("//div[@class='nameTitle']/text()").extract()
        listed_by = listed_by[0]
        property_type = "Paying-Guest"
        posted_date = response.xpath("//div[@class='postedOn']/text()").extract()
        posted_date = posted_date[0].strip()
        posted_date = re.sub('Posted on:','',posted_date).strip()
        name = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='name']/@content").extract()
        file_id = response.meta['file_id']

        prop_details['prop_id'] = prop_id
        if property_url:
            prop_details['property_url'] = property_url[0].strip()
        if file_id:
            prop_details['file_id'] = file_id
        if listed_by:
            prop_details['listed_by'] = listed_by
        if property_type:
            prop_details['property_type'] = property_type
        if posted_date:
            prop_details['posted_date'] = posted_date
        if name:
            prop_details['name'] = name[0]
        
        #Location

        city = response.xpath("//div[@itemtype='http://schema.org/PostalAddress']/meta[@itemprop='addressRegion']/@content").extract()
        locality = response.xpath("//div[@itemprop='address']/meta[@itemprop='addressLocality']/@content").extract()
        address = response.xpath("//div[@class='p_title'][text()='Address']/following-sibling::div[@class='p_value']/text()").extract()
        landmark = response.xpath("//div[@class='p_title'][text()='Landmarks']/following-sibling::div[@class='p_value']/text()").extract()
        latitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='latitude']/@content").extract()
        longitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='longitude']/@content").extract()

        if city:
            prop_details['city'] = city[0]
        if locality:
            prop_details['locality'] = locality[0]
        if address:
            prop_details['address'] = address[0]
        if landmark:
            prop_details['landmark'] = landmark[0]
        if latitude:
            prop_details['latitude'] = latitude[0]
        if longitude:
            prop_details['longitude'] = longitude[0]
        try:
            geohash = Geohash.encode(float(prop_details['latitude']), float(prop_details['longitude']), precision=9)
        except ValueError:
            pass
        if geohash:
            prop_details['geohash'] = geohash


        #Property Features

        bhk = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='numberOfRooms']/@content").extract()
        bathrooms = response.xpath("//div[@class='p_title' and contains(text(),'Bathroom')]/following-sibling::div[@class='p_value']/text()").extract()
        bedroom_dimensions = response.xpath("//span[@class='ftrt bedroomVal']/text()").extract()
        #balcony = response.xpath("//div[@class='p_title' and contains(text(),'Balcon')]/following-sibling::div[@class='p_value']/text()").extract()
        furnished_status = response.xpath("//div[@class='p_title' and contains(text(),'Furnished status')]/following-sibling::div[@class='p_value']/text()").extract()
        floor = response.xpath("//div[@class='p_title'][text()='Floor']/following-sibling::div[@class='p_value truncated']/text()").extract()
    
        if floor != []:
            if 'Ground' in floor[0] or 'Lower Basement' in floor[0] or 'Upper Basement' in floor[0]:
                floor_num = "Ground"                                           #floor_num is string
            #total_floors = re.findall(r'\b\d+\b', floor)
            #total_floors = int(total_floors[0])
            elif floor != []:
                floor_num = re.findall(r'\b\d+\b',floor[0])
            #total_floors = int(floor_num[1])
        else:
            floor_num = "Not Specified"

        if bhk:
            prop_details['bhk'] = bhk[0]
        if bedroom_dimensions:
            prop_details['bedroom_dimensions'] = bedroom_dimensions[0]
        if furnished_status:
            prop_details['furnished_status'] = furnished_status[0]
        if bathrooms:
            prop_details['bathrooms'] = bathrooms[0]
        if balcony:
            prop_details['balconies'] = balcony[0]
        if floor_num:
            prop_details['floor_num'] = floor_num[0]

        #Rent Details
        rent = response.xpath("//div[@itemtype='http://schema.org/PriceSpecification']/meta[@itemprop='price']/@content").extract()
        if rent != []:
            rent = re.sub(',','',rent[0])
            if 'Lac' in rent or 'Cr' in rent:
                if 'Lac' in rent:
                    rent = re.sub('Lac','',rent).strip()
                    rent = int(float(rent))
                    rent = rent*10**5
                elif 'Cr' in rent:
                    rent = re.sub('Cr','',rent).strip()
                    rent = int(float(rent))
                    rent = rent*10**7

        security_deposit = response.xpath("//div[@class='applicableCharges']/div[@class='tr']/div[@class='td' and contains(text(),'Security Deposit')]/following-sibling::div[@class='td']/text()").extract()
        if security_deposit != []:
                security_deposit = re.sub(',','',security_deposit[0])
                security_deposit = re.findall(r'\b\d+\b', security_deposit)
                security_deposit = int(security_deposit[0])
        one_time_maintenance = response.xpath("//div[@class='td' and contains(text(),'Maintenance')]/following-sibling::div[@class='td']/text()").extract()
        if one_time_maintenance:
            one_time_maintenance = one_time_maintenance[0]
            one_time_maintenance = one_time_maintenance.split(" ")[1]
            one_time_maintenance = int(re.sub(',','',one_time_maintenance))
        if rent:
            prop_details['rent'] = rent
        if security_deposit:
            prop_details['security_deposit'] = security_deposit
        if one_time_maintenance:
            prop_details['one_time_maintenance'] = one_time_maintenance

        if listed_by == 'Agent':
            agent_name = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/div[@class='agentName']/text()").extract()
            agent_operation_year = response.xpath("//div[@class='agentOperateVal']/text()").extract()
            agent_address = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/p[@class='agentCategory' and contains(.,'Location')]/text()").extract()
            agent_dealing_in = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/p[@class='agentCategory' and contains(.,'Dealing')]/text()").extract()
            agent_url = response.xpath("//div[@class='agentInfoL']/a/@href").extract()
            if 'owner' in agent_url[0]:
                agent_url = re.sub('owner','agent',agent_url[0])
            agent_prop_url = response.xpath("//div[@class='agentPropCountWrap']/a/@href").extract()[0]
            agent_prop_url = 'https://www.magicbricks.com' + agent_prop_url
            agent_prop_count = response.xpath("//div[@class='agentPropCount sale']/text()").extract()


            if agent_name:
                prop_details['agent_name'] = agent_name[0]
            if agent_url:
                prop_details['agent_url'] = agent_url
            if agent_operation_year:
                prop_details['agent_operation_year'] = agent_operation_year[0]
            if agent_address:
                prop_details['agent_address'] = agent_address[0]
            if agent_dealing_in:
                prop_details['agent_dealing_in'] = agent_dealing_in[0]
            if agent_prop_url:
                prop_details['agent_prop_url'] = agent_prop_url
            if agent_prop_count:
                prop_details['agent_prop_count'] = agent_prop_count[0]

        elif listed_by == "Owner":
            #Owmner
            owner_name = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/div[@class='agentName']/text()").extract()
            if owner_name:
                prop_details['owner_name'] = owner_name

        elif listed_by == "Builder":
            #Builder
            builder_name = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/div[@class='agentName']/text()").extract()
            if builder_name:
                prop_details['builder_name'] = builder_name
        else:
            c=c+1

        # Project-Details
        """project_name = response.xpath("//div[@class='p_title' and contains(text(),'Society')]/following-sibling::div[@class='p_value']/a/text()").extract()
        developer_name = response.xpath("//div[@class='devName']")
        project_url= response.xpath("//div[@class='p_title' and contains(text(),'Society')]/following-sibling::div[@class='p_value']/a/@href").extract()

        if project_name:
            prop_details['project_name'] = project_name[0]
        if developer_name:
            prop_details['developer_name'] = developer_name[0]
        if project_url:
            prop_details['project_url'] = project_url[0]"""
        
        #Other Details
        rooms_in_pg = response.xpath("//div[@class='p_title'][text()='Rooms in PG']/following-sibling::div[@class'p_value']/text()").extract()
        water_availability = response.xpath("//div[@class='p_title' and contains(text(),'Water Availability')]/following-sibling::div[@class='p_value']/text()").extract()        
        lift = response.xpath("//div[@class='p_title'][text()='Lift']/following-sibling::div[@class='p_value']/text()").extract()
        facing = response.xpath("//div[@class='p_title'][text()='Facing']/following-sibling::div[@class='p_value']/text()").extract()        
        electricity_availability = response.xpath("//div[@class='p_title'][text()='Status of Electricity']/following-sibling::div[@class='p_value']/text()").extract()
        overlooking = response.xpath("//div[@class='p_title'][text()='Overlooking']/following-sibling::div[@class='p_value']/text()").extract()        
        preferences = response.xpath("//div[@class='p_title'][text()='Other Tenants Preferred']/following-sibling::div[@class='p_value']/text()").extract()
        meals_included = response.xpath("//div[@class='p_title'][text()='Meals Included']/following-sibling::div[@class'p_value']/text()").extract()
        ac = response.xpath("//div[@class='p_title'][text()='AC']/following-sibling::div[@class'p_value']/text()").extract()
        wifi = response.xpath("//div[@class='p_title'][text()='Wifi']/following-sibling::div[@class'p_value']/text()").extract()
        attached_bathroom = response.xpath("//div[@class='p_title'][text()='Attached Bathroom']/following-sibling::div[@class'p_value']/text()").extract()
        timing_restriction = response.xpath("//div[@class='p_title'][text()='Timing restriction']/following-sibling::div[@class'p_value']/text()").extract()
        notice_period = response.xpath("//div[@class='p_title'][text()='Notice Period']/following-sibling::div[@class'p_value']/text()").extract()

        if notice_period:
            prop_details['notice_period'] = notice_period[0]
        if attached_bathroom:
            prop_details['attached_bathroom'] = attached_bathroom[0]
        if timing_restriction:
            prop_details['timing_restriction'] = timing_restriction[0]
        if ac:
            prop_details['ac'] = ac[0]
        if wifi:
            prop_details['wifi'] = wifi[0]
        if meals_included:
            prop_details['meals_included'] = meals_included[0]
        if preferences:
            prop_details['preferences'] = preferences[0]
        if tenants_preferred:
            prop_details['tenants_preferred'] = tenants_preferred[0]
        if electricity_availability:
            prop_details['electricity_availability'] = electricity_availability[0]
        if water_availability:
            prop_details['water_availability'] = water_availability[0]
        if facing:
            prop_details['facing'] = facing[0]
        if overlooking:
            prop_details['overlooking'] = overlooking[0]
        if lift:
            prop_details['lift'] = lift[0]

        #prop['amenities'] = amenities
        Property['prop_details'] = prop_details

        file = 'parsed/rent/pg/%s/%s' % (response.meta['city'],response.meta['file_id'])
        save_obj(Property, file)