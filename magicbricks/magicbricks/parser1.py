import scrapy
import pickle
import os
import re
import js2xml

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

def price_to_decimal(price, price_unit):
    if price_unit == 'Lac' or price_unit =='L':
        return price*10**5
    elif price_unit == 'Crore' or price_unit =='Cr':
        return price*10**7

root = '/Users/varshathanooj/Documents/GitHub/Flatopedia/magicbricks'

class MagicBricks(scrapy.Spider):
    
    name = "parser_projects"
    projects = {}

    def start_requests(self):
        cities = load_obj('cities')
        for city in cities:
            if not os.path.exists('html/projects_html'+city):
                continue

            if not os.path.exists('parsed/'+city):
                os.makedirs('parsed/'+city)

            for file in os.listdir('html/projects_html'+city):
                project_id = file
                url = 'file://%s/html/projects_html/%s/%s' % (root,city,file)

                yield scrapy.Request(url=url, callback=self.parse, meta={'project_id':project_id, 'city':city 'url':url})
               
    def parse(self, response):
        project_details = {}
        project = {}
        project_id = response.meta['project_id']
        project_details['project_id'] = project_id
        project_url = response.meta['url']
        project_details['project_url'] = project_url
        #project details
        project_name = response.xpath("//div[@class='h1Block']/h1/text()").extract()
        locality = response.xpath("//div[@itemprop='address']/meta[@itemprop='addressLocality']/data(@content)").extract()
        city = respone.xpath("//div[@itemprop='address']/meta[@itemprop='addressRegion']/data(@content)").extract()
        latitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='latitude']/data(@content)").extract()
        longitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='longitude']/data(@content)").extract()
        status = response.xpath("//div[@class='newPiceBlockSec sec4']/div[@class='secValueUp']/span/text()").extract()
        units = response.xpath("//div[@class='infoList']/span/text()").extract()[0]
        towers = response.xpath("//div[@class='infoList']/span/text()").extract()[1]

        builder_name = response.xpath("//script/[var='buildername']").extract()
        parsed_js = js2xml.parse(builder_name)
        js_sel = scrapy.Selector(_root=parsed_js)
        builder_name = js_sel.xpath("//program/var[@name='buildername']/string/@value")




        min_price = response.xpath("//meta[@itemProp='minPrice']/data(@content)").extract()
        if 'Lac' in min_price:
            min_price = float(re.sub('Lac','',min_price).strip())
        max_price = response.xpath("//meta[@itemProp='maxPrice']/data(@content)").extract()
        if 'Lac' in max_price:
            max_price = float(re.sub('Lac','',max_price)).strip()
        elif 'Cr' in max_price:
            max_price = float(re.sub('Cr','',max_price)).strip()

        if min_price == "":
            min_price = response.xpath("//div[@class='projectPrice']/text()")
            min_price = re.
            max_price = "Not Specified"


        t1 = response.xpath("//div[@class='secSubUp']/text()").extract()
        #min_price_per_sqft = t1[t1.index(t1[5]):t1.index("-")]
        t1 = re.sub(',','',t1).strip()
        p = re.compile('\d+')
        p = p.findall(t1)
        if p[0]:
            min_price_per_sqft = p[0]
        if p[1]:
            max_price_per_sqft = p[1]

        if project_name:
            project_details['project_name'] = project_name[0]
        if locality:
            project_details['locality'] = locality[0]
        if city:
            project_details['city'] = city[0]
        if latitude:
            project_details['latitude'] = latitude[0]
        if longitude:
            project_details['longitude'] = longitude[0]
        if min_price:
            min_price = float(min_price[0])
            project_details['min_price'] = min_price
        if max_price:
            max_price = float(max_price[0])
            project_details['max_price'] = max_price
        if builder_name:
            project_details['builder_name'] = builder_name[0]
        if min_price_per_sqft:
            project_details['min_price_per_sqft'] = min_price_per_sqft
        if max_price_per_sqft:
            project_details['max_price_per_sqft'] = max_price_per_sqft
        if status:
            project_details['status'] = status[0]
        if units:
            project_details['units'] = units[0]
        if towers:
            project_details['towers'] = towers[0]



        #amenities
        amenities_list = response.xpath("//span[@class='ameLabel']/text()").extract()
        amenities_list = [amenity.strip() for amenity in amenities_list if amenity.strip()]
        amenities = {}
        for amenity in amenities_list:
            amenities[amenity] = True
        project['amenities'] = amenities
        project['project_details'] = project_details
        project['floor_plan'] = floor_plan