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
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def price_to_decimal(price):
    if 'Lac' in price:
        price = re.sub('Lac','',price).strip()
        price = float(price)
        return int(price*10**5)
    elif 'Cr' in price:
        price = re.sub('Cr','',price).strip()
        price = float(price)
        return int(price*10**7)
    else:
        price = re.sub(',','',price)
        return int(price)

root = '/Users/varshathanooj/Desktop/magicbrick'

class MagicBricks(scrapy.Spider):
    name = "parser_projects"

    def start_requests(self):
        cities = load_obj('cities')
        for city in cities:
            if not os.path.exists('html/projects_html/'+city):
                continue

            if not os.path.exists('parsed/projects/'+city):
                os.makedirs('parsed/projects/'+city)

            for file in os.listdir('html/projects_html/'+city):
                file_id = file
                url = 'file://%s/html/projects_html/%s/%s' % (root,city,file)

                yield scrapy.Request(url=url, callback=self.parse, meta={ 'city':city,'url':url, 'file_id':file_id})
               
    def parse(self,response):
        project = {}
        project_details = {}
        amenities = {}
        file_id = response.meta['file_id']
        project_name = response.xpath("//div[@itemtype='http://schema.org/ApartmentComplex']/meta[@itemprop='name']/@content").extract()
        project_url = response.xpath("//link[@rel='canonical']/@href").extract()
        price_check = response.xpath("//div[@class='projectPrice']/text()").extract()
        if price_check != []:
            if 'Onwards' in price_check[0]:
                price_check = re.sub(' Onwards','',price_check[0]).strip()
                price_check = price_to_decimal(price_check)
                min_price = price_check
                max_price = price_check
            else:
                min_price = response.xpath("//div[@itemtype='http://schema.org/PriceSpecification']/meta[@itemprop='minPrice']/@content").extract()
                max_price = response.xpath("//div[@itemtype='http://schema.org/PriceSpecification']/meta[@itemprop='maxPrice']/@content").extract()
                try:
                    min_price = price_to_decimal(min_price[0])
                    max_price = price_to_decimal(max_price[0])
                except IndexError:
                    pass
        latitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='latitude']/@content").extract()
        longitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='longitude']/@content").extract()
        city = response.xpath("//div[@itemtype='http://schema.org/PostalAddress']/meta[@itemprop='addressRegion']/@content").extract()
        locality = response.xpath("//div[@itemtype='http://schema.org/PostalAddress']/meta[@itemprop='addressLocality']/@content").extract()
        status = response.xpath("//div[@class='secHeaderUp'][text()='Status']/following-sibling::div[@class='secValueUp']/span/text()").extract()
        infoList = response.xpath("//div[@class='infoList']/span/text()").extract()
        if infoList !=[]:
            try:
                units = infoList[0]
                towers = infoList[1]
                if units:
                    project_details['units'] = units
                if towers:
                    project_details['towers'] = towers
            except IndexError:
                pass

        # Amenities
        amenities1 = response.xpath("//div[@id='normalAminities']/ul/li/div[@class='clearAll']/following-sibling::span/text()").extract()
        amenities2 = response.xpath("//div[@id='normalAminities']/ul/span[@class='hidddenAminities']/li/div[@class='clearAll']/following-sibling::span/text()").extract()
        amenities1 = [str(amenity) for amenity in amenities1 if not 'No' in amenity]
        amenities2 = [str(amenity) for amenity in amenities2 if not 'No' in amenity]
        amenities_total = amenities1 + amenities2
        if amenities_total:
            for amenity in amenities_total:
                amenities[amenity] = True
            project['amenities'] = amenities_total

        title = response.xpath("//title/text()").extract()

        a = response.xpath("//div[@class='propDtls']/div[@class='bed']/text()").extract()
        if a != []:
            try:
                b = [re.findall(r'\b\d+\b',bed) for bed in a]
                bhk=[]
                for i in range(len(b)):
                    bhk.append(int(b[i][0].strip()))
                bhk = list(set(bhk))
                bhk.sort()
                if bhk:
                    project_details['bhk'] = bhk
            except IndexError:
                pass
        try:
            if 'Residential Plot' in a[0]:
                property_type = 'Residential Plot'
            elif 'Flat' in a[0]:
                property_type = 'Apartment'
            elif 'Apartment' in a[0]:
                property_type = 'Apartment'
            elif 'Commercial' in a[0]:
                property_type = 'Commercial Space'
            elif 'Villa' in a[0]:
                property_type = 'Villa'
            else:
                property_type = 'NA'
            if property_type:
                project_details['property_type'] = property_type
        except IndexError:
            pass

        area = response.xpath("//div[@class='propDtls']/div[@class='space']/text()").extract()
        if area !=[]:
            area = [re.sub(' sqft','',a) for a in area]
            min_area = min(area)
            max_area = max(area)
            if min_area:
                project_details['min_area'] = min_area
            if max_area:
                project_details['max_area'] = max_area
        try:
            developer_name = response.xpath("//div[@id='otherProjectsByDeveloper']").extract()[0]
            developer_name = developer_name[developer_name.index('&devName=')+len('&devName='):developer_name.index('&cityName')].strip()
            if developer_name:
                project_details['developer_name'] = developer_name
        except IndexError:
            pass
        if project_name:
            project_details['project_name'] = project_name[0].strip()
        if file_id:
            project_details['file_id'] = file_id
        if project_url:
            project_details['project_url'] = project_url[0]
        if min_price:
            project_details['min_price'] = min_price
        if max_price:
            project_details['max_price'] = max_price
        if latitude:
            project_details['latitude'] = latitude[0]
        if longitude:
            project_details['longitude'] = longitude[0]
        if city:
            project_details['city'] = city[0]
        if locality:
            project_details['locality'] = locality[0]
        if status:
            project_details['status'] = status[0]
        if title:
            project_details['title'] = title[0]
        try:
            geo_hash = Geohash.encode(float(project_details['latitude']), float(project_details['longitude']), precision=9)
        except ValueError:
            pass
        if geo_hash:
            project_details['geo_hash'] = geo_hash

        project['project_details'] = project_details
        file = 'parsed/projects/%s/%s' % (response.meta['city'],response.meta['file_id'])
        save_obj(project, file)