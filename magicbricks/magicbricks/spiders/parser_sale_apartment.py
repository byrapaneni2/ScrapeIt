import scrapy
import pickle
import os
import re
import json
import shutil
import Geohash
import dateparser
from datetime import datetime

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

root = '/Users/varshathanooj/Documents/GitHub/Flatopedia/magicbricks'


class MagicBricks(scrapy.Spider):
    name = "parser_sale_apartment"

    def start_requests(self):
        #cities = load_obj('cities')
        cities = ['Agra']
        for city in cities:
            if not os.path.exists('html/sale_html/apartment/'+city):
                continue

            if not os.path.exists('parsed/sale/apartment/'+city):
                os.makedirs('parsed/sale/apartment/'+city)

            for file in os.listdir('html/sale_html/apartment/'+city):
                file_id = file
                url = 'file://%s/html/sale_html/apartment/%s/%s' % (root,city,file)

                yield scrapy.Request(url=url, callback=self.parse, meta={ 'city':city,'url':url, 'file_id':file_id})
               
    def parse(self,response):
        prop_details = {}
        Property= {}
        #Basic Details
        prop_id = response.xpath("//div[@class='propertyId']/text()").extract()
        prop_id = re.findall(r'\b\d+\b',prop_id[0])
        prop_id = int(prop_id[0])
        property_url = response.xpath("//link[@rel='canonical']/@href").extract()
        property_url = property_url[0].strip()
        if 'Multistorey-Apartment' in property_url:
			property_type = "Multistorey-Apartment"
			name = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='name']/@content").extract()
			bhk = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='numberOfRooms']/@content").extract()
			covered_area = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='floorSize']/@content").extract()
			if covered_area != []:
				covered_area = re.findall(r'\b\d+\b', covered_area[0])
				covered_area = int(covered_area[0])
			description = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='description']/@content").extract()
        elif 'Builder-Floor-Apartment' in property_url:
			property_type = "Builder-Floor-Apartment"
			name = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='name']/@content").extract()
			bhk = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='numberOfRooms']/@content").extract()
			covered_area = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='floorSize']/@content").extract()
			if covered_area != []:
				covered_area = re.findall(r'\b\d+\b', covered_area[0])
				covered_area = int(covered_area[0])
			description = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='description']/@content").extract()
        elif 'Studio-Apartment' in property_url:
			property_type = "Studio-Apartment"
			name = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='name']/@content").extract()
			bhk = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='numberOfRooms']/@content").extract()
			covered_area = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='floorSize']/@content").extract()
			if covered_area != []:
				covered_area = re.findall(r'\b\d+\b', covered_area[0])
				covered_area = int(covered_area[0])
			description = response.xpath("//div[@itemtype='http://schema.org/SingleFamilyResidence']/meta[@itemprop='description']/@content").extract()
        else:
			property_type = "Others"

        listed_by = response.xpath("//div[@class='nameTitle']/text()").extract()
        listed_by = listed_by[0]
        posted_date = response.xpath("//div[@class='postedOn']/text()").extract()
        posted_date = posted_date[0].strip()
        posted_date = str(re.sub('Posted on:','',posted_date).strip())
        posted_date = re.sub("'","",posted_date)
        posted_date = dateparser.parse(posted_date)
        posted_date = str(posted_date)

        
        file_id = response.meta['file_id']

        prop_details['prop_id'] = prop_id
        if property_url:
            prop_details['property_url'] = property_url
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
            prop_details['address'] = address[0].strip()
        if landmark:
            prop_details['landmark'] = landmark[0]
        if latitude:
            prop_details['latitude'] = latitude[0]
        if longitude:
            prop_details['longitude'] = longitude[0]
        try:
            geo_hash = Geohash.encode(float(prop_details['latitude']), float(prop_details['longitude']), precision=9)
        except ValueError:
            pass
        if geo_hash:
            prop_details['geo_hash'] = geo_hash


        #Property Features

        carpet_area = response.xpath("//span[@id='carpetAreaDisplay']/text()").extract()
        carpet_area = int(carpet_area[0])
        bathrooms = response.xpath("//div[@class='p_title' and contains(text(),'Bathroom')]/following-sibling::div[@class='p_value']/text()").extract()
        bedroom_dimensions = response.xpath("//span[@class='ftrt bedroomVal']/text()").extract()
        balcony = response.xpath("//div[@class='p_title' and contains(text(),'Balcon')]/following-sibling::div[@class='p_value']/text()").extract()
        furnished_status = response.xpath("//div[@class='p_title' and contains(text(),'Furnished status')]/following-sibling::div[@class='p_value']/text()").extract()
        floor = response.xpath("//div[@class='p_title'][text()='Floor']/following-sibling::div[@class='p_value truncated']/text()").extract()
        #bedrooms = response.xpath("//div[@class='p_title'][text()='Bedrooms']/following-sibling::div[@class='p_value']").extract()
        #note = response.xpath("//div[@class='tr chargesNote']/p/text()").extract()
        #units_on_floor = response.xpath("//div[@class='p_title'][text()='Units on Floor']/following-sibling::div[@class='p_value']/text()").extract()
        if floor != []:
            if 'Ground' in floor[0] or 'Lower Basement' in floor[0] or 'Upper Basement' in floor[0]:
                floor_num = "Ground"                                         #floor_num is string
            #total_floors = re.findall(r'\b\d+\b', floor)
            #total_floors = int(total_floors[0])
            elif floor != []:
                floor_num = re.findall(r'\b\d+\b',floor[0])
                floor_num = floor_num[0]
                #total_floors = int(floor_num[1])
        else:
            floor_num = "Not Specified"

        if bhk:
            prop_details['bhk'] = int(bhk[0])
        if bedroom_dimensions:
            prop_details['bedroom_dimensions'] = bedroom_dimensions[0]
        if furnished_status:
            prop_details['furnished_status'] = furnished_status[0]
        if bathrooms:
            prop_details['bathrooms'] = int(bathrooms[0])
        if balcony:
            prop_details['balcony'] = int(balcony[0])
        if floor_num:
            prop_details['floor_num'] = floor_num

        #Area
        if carpet_area:
            prop_details['carpet_area'] = carpet_area
        if covered_area:
            prop_details['covered_area'] = covered_area

        #Property Availability
    

        age_of_construction = response.xpath("//div[@class='p_title'][text()='Age of Construction']/following-sibling::div[@class='p_value']/text()").extract()
        status = response.xpath("//div[@class='p_title'][text()='Status']/following-sibling::div[@class='p_value']/text()").extract()
        transaction_type = response.xpath("//div[@class='p_title'][text()='Transaction type']/following-sibling::div[@class='p_value']/text()").extract()
        type_of_ownership = response.xpath("//div[@class='p_title'][text()='Type of Ownership']/following-sibling::div[@class='p_value']/text()").extract()
        if status != []:
	        if status[0] == 'Under Construction':
	        	posession_by = response.xpath("//div[@class='p_title' and contains(text(),'Posession')]/following-sibling::div[@class='p_value']/text()").extract()
	        	if posession_by != []:
	        		posession_by = re.sub("'","",posession_by[0].strip())
	        		posession_by = dateparser.parse(posession_by)
	        		posession_by = str(posession_by)
	        	if posession_by:
	        		prop_details['posession_by'] = posession_by

        if age_of_construction:
            prop_details['age_of_construction'] = age_of_construction[0]
        if status:
            prop_details['status'] = status[0].strip()
        if transaction_type:
            prop_details['transaction_type'] = transaction_type[0]
        if type_of_ownership:
            prop_details['type_of_ownership'] = type_of_ownership[0]
        

        c=0
        #Rent Details
        price = response.xpath("//div[@itemtype='http://schema.org/PriceSpecification']/meta[@itemprop='price']/@content").extract()
        try:
	        if price != []:
	            if 'Lac' in price[0] or 'Cr' in price[0]:
	                if 'Lac' in price[0]:
	                    price = re.sub('Lac','',price[0]).strip()
	                    price = float(price)
	                    price = int(price*10**5)
	                elif 'Cr' in price[0]:
	                    price = re.sub('Cr','',price[0]).strip()
	                    price = float(price)
	                    price = int(price*10**7)
                    else:
		            	price = re.sub(',','',price[0])
		            	price = int(price)
        except:
        	price = 0

        """monthly_maintainance = response.xpath("//div[@class='td' and contains(text(),'Maintenance')]/following-sibling::div[@class='td']/text()").extract()
        if monthly_maintainance:
            monthly_maintainance = monthly_maintainance[0]
            monthly_maintainance = monthly_maintainance.split(" ")[1]
            monthly_maintainance = int(re.sub(',','',monthly_maintainance))"""
        if price:
            prop_details['price'] = price

        if listed_by == 'Agent':
            agent_name = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/div[@class='agentName']/text()").extract()
            agent_operation_year = response.xpath("//div[@class='agentOperateVal']/text()").extract()
            agent_address = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/p[@class='agentCategory' and contains(.,'Location')]/text()").extract()
            agent_dealing_in = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/p[@class='agentCategory' and contains(.,'Dealing')]/text()").extract()
            agent_url = response.xpath("//div[@class='agentInfoL']/a/@href").extract()
            if agent_url != []:
                if 'owner' in agent_url[0]:
                    agent_url = re.sub('owner','agent',agent_url[0])
            agent_prop_url = response.xpath("//div[@class='agentPropCountWrap']/a/@href").extract()
            if agent_prop_url !=[]:
                agent_prop_url = 'https://www.magicbricks.com' + agent_prop_url[0]
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
                prop_details['owner_name'] = owner_name[0]

        elif listed_by == "Builder":
            #Builder
            builder_name = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/div[@class='agentName']/text()").extract()
            if builder_name:
                prop_details['builder_name'] = builder_name[0]
        else:
            c=c+1
            

        
        
        

        # Project-Details

        project_name = response.xpath("//div[@class='p_title' and contains(text(),'Society')]/following-sibling::div[@class='p_value']/span[@class='prop_address']/a/text()").extract()
        developer_name = response.xpath("//div[@class='devName']/text()").extract()
        if developer_name != []:
            developer_name = re.sub('Developed/built by ','',developer_name[0])
        project_url= response.xpath("//div[@class='p_title' and contains(text(),'Society')]/following-sibling::div[@class='p_value']/span[@class='prop_address']/a/@href").extract()
        
        #Other Details
        
        car_parking = response.xpath("//div[@class='p_title' and contains(text(),'Car parking')]/following-sibling::div[@class='p_value']/text()").extract()
        water_availability = response.xpath("//div[@class='p_title' and contains(text(),'Water Availability')]/following-sibling::div[@class='p_value']/text()").extract()        
        facing = response.xpath("//div[@class='p_title'][text()='Facing']/following-sibling::div[@class='p_value']/text()").extract()        
        electricity_availability = response.xpath("//div[@class='p_title'][text()='Status of Electricity']/following-sibling::div[@class='p_value']/text()").extract()
        flooring = response.xpath("//div[@class='p_title'][text()='Flooring']/following-sibling::div[@class='p_value']/text()").extract()
        overlooking = response.xpath("//div[@class='p_title'][text()='Overlooking']/following-sibling::div[@class='p_value']/text()").extract()
        #authority_approval = response.xpath("//div[@class='p_title'][text()='Authority Approval']/following-sibling::div[@class='p_value']/text()").extract()
        #furnishing_details = response.xpath("//div[@class='p_title'][text()='Furnishing Details']/following-sibling::div[@class='p_value']/div[@class='amenities']").extract()
        #furnishing_details = [f.strip() for f in furnishing_details]
        if description:
            prop_details['description'] = description[0]
        if project_name:
            prop_details['project_name'] = project_name[0]
        if developer_name:
            prop_details['developer_name'] = developer_name
        if project_url:
            prop_details['project_url'] = project_url[0]
        if flooring:
            prop_details['flooring'] = flooring[0]
        if electricity_availability:
            prop_details['electricity_availability'] = electricity_availability[0]
        if water_availability:
            prop_details['water_availability'] = water_availability[0]
        if facing:
            prop_details['facing'] = facing[0]
        if car_parking:
            prop_details['car_parking'] = car_parking[0]

        #Property['multistorey_amenities'] = amenities
        Property['prop_details'] = prop_details
        file = 'parsed/sale/apartment/%s/%s' % (response.meta['city'],response.meta['file_id'])
        save_obj(Property, file)