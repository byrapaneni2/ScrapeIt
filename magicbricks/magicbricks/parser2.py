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

def hasXpath(xpath):
    try:
        self.browser.find_element_by_xpath(xpath)
        return True
    except:
        return False

root = '/Users/varshathanooj/Documents/GitHub/Flatopedia/magicbricks'

class MagicBricks(scrapy.Spider):
    
    name = "parser_rent"
    projects = {}

    def start_requests(self):
        cities = load_obj('cities')
        for city in cities:
            if not os.path.exists('html/rent_html'+city):
                continue

            if not os.path.exists('parsed/'+city):
                os.makedirs('parsed/'+city)

            for file in os.listdir('html/rent_html'+city):
                property_id = file
                url = 'file://%s/html/rent_html/%s/%s' % (root,city,file)

                yield scrapy.Request(url=url, callback=self.parse, meta={'property_id':property_id, 'city':city 'url':url})
               
    def parse(self, response):
        property_details = {}
        prop= {}
        prop_id = response.xpath("//div[@class='propertyId]/text()").extract()
        prop_id = prop_id.split(" ")[2]
        listed_by = response.xpath("//div[@class='nameTitle']/text()")
        name = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='name']/data(@content)")
        description = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='description']/data(@content)")
        rent = response.xpath("//div[@itemtype='http://schema.org/PriceSpecification']/meta[@itemprop='price']/data(@content)").extract()
        deposit = response.xpath("//div[@class='deposit']/text()").extract()
        bhk = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='numberOfRooms']/data(@content)")
        area = response.xpath("//div[@itemtype='http://schema.org/Apartment']/meta[@itemprop='floorSize']/data(@content)").extract()
        area = area.split(" ")[0]
        note = response.xpath("//div[@class='tr chargesNote']/p/text()")

        #agent
        agent_name = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/div[@class='agentName']/text()").extract()
        agent_operation_year = response.xpath("//div[@class='agentOperateVal']/text()").extract()
        agent_address = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/p[@class='agentCategory' and contains(.,'Location')]/text()").extract()
        agent_dealing_in = response.xpath("//div[@class='agentInfo']/div[@class='agentInfoL']/p[@class='agentCategory' and contains(.,'Dealing')]/text()").extract()
        agent_url = response.xpath("//div[@class='agentInfoL']/a/data(@href)")
        if 'owner' in agent_url:
            agent_url = re.sub('owner','agent',agent_url)
        agent_prop_url = response.xpath("//div[@class='agentPropCountWrap']/a/data(@href)").extract()[0]
        agent_prop_url = 'https://www.magicbricks.com' + agent_prop_url
        agent_prop_count = response.xpath("//div[@class='agentPropCount sale']/text()").extract()




        locality = response.xpath("//div[@itemprop='address']/meta[@itemprop='addressLocality']/data(@content)").extract()
        city = respone.xpath("//div[@itemprop='address']/meta[@itemprop='addressRegion']/data(@content)").extract()
        address = response.xpath("//div[@class='p_title'][text()='Address']/following-sibling::div[@class='p_value']/text()").xpath()
        landmark = response.xpath("//div[@class='p_title'][text()='Landmarks']/following-sibling::div[@class='p_value']/text()").xpath()
        latitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='latitude']/data(@content)").extract()
        longitude = response.xpath("//div[@itemprop='geo']/meta[@itemprop='longitude']/data(@content)").extract()
        posted_date = response.xpath("//div[@class='postedOn']/text()")
        bathrooms = response.xpath("//div[@class='p_title' and contains(text(),'Bathrooms')]/following-sibling::div[@class='p_value']/text()").extract()
        balconies = response.xpath("//div[@class='p_title' and contains(text(),'Balconies')]/following-sibling::div[@class='p_value']/text()").extract()
        store_room = response.xpath("//div[@class='p_title' and contains(text(),'Store Room')]/following-sibling::div[@class='p_value']/text()").extract()
        society = response.xpath("//div[@class='p_title' and contains(text(),'Society')]/following-sibling::div[@class='p_value']/a/text()").extract()
        project_url= response.xpath("//div[@class='p_title' and contains(text(),'Society')]/following-sibling::div[@class='p_value']/a/data(@href)").extract()
        furnished_status = response.xpath("//div[@class='p_title' and contains(text(),'Furnished status')]/following-sibling::div[@class='p_value']/text()").extract()
        car_parking = response.xpath("//div[@class='p_title' and contains(text(),'Car parking')]/following-sibling::div[@class='p_value']/text()").extract()
        tenants_preferred = response.xpath("//div[@class='p_title'][text()='Tenants Preferred']/following-sibling::div[@class='p_value']/text())").extract()
        water_availability = response.xpath("//div[@class='p_title' and contains(text(),'Water Availability')]/following-sibling::div[@class='p_value']/text()").extract()
        floor = response.xpath("//div[@class='p_title'][text()='Floor']/following-sibling::div[@class='p_value truncated']/text()").extract()
        units_on_floor = response.xpath("//div[@class='p_title'][text()='Units on Floor']/following-sibling::div[@class='p_value']/text()").extract()
        lift = response.xpath("//div[@class='p_title'][text()='Lift']/following-sibling::div[@class='p_value']/text()").extract()
        facing = response.xpath("//div[@class='p_title'][text()='Facing']/following-sibling::div[@class='p_value']/text()").extract()
        status = response.xpath("//div[@class='p_title'][text()='Status']/following-sibling::div[@class='p_value']/text()").extract()
        electricity_availability = response.xpath("//div[@class='p_title'][text()='Status of Electricity']/following-sibling::div[@class='p_value']/text()").extract()
        water_availability = response.xpath("//div[@class='p_title'][text()='Water Availability']/following-sibling::div[@class='p_value']").extract()
        flooring = response.xpath("//div[@class='p_title'][text()='Flooring']/following-sibling::div[@class='p_value']/text()").extract()
        overlooking = response.xpath("//div[@class='p_title'][text()='Overlooking']/following-sibling::div[@class='p_value']/text()").extract()
        construction_age = response.xpath("//div[@class='p_title'][text()='Age of Construction']/following-sibling::div[@class='p_value']/text()").extract()
        preferences = response.xpath("//div[@class='p_title'][text()='Other Tenants Preferred']/following-sibling::div[@class='p_value']/text()").extract()
        authority_approval = response.xpath("//div[@class='p_title'][text()='Authority Approval']/following-sibling::div[@class='p_value']/text()").extract()
        furnishing_details = response.xpath("//div[@class='p_title'][text()='Furnishing Details']/following-sibling::div[@class='p_value']/div[@class='amenities']").extract()
        furnishing_details = [f.strip() for f in furnishing_details]
        magicbricks_verified = hasXpath('//div[@class='propVerifiedParent']/div[@class='propVerified']')

        #amenities
        amenities = response.xpath("//div[@class='p_title'][text()='Amenities']/following-sibling::div[@class='p_value']/div[@class='amenities']/ul/li").extract()
        amenities = [amenity.strip() for amenity in amenities]


        #property_details

        prop_details['prop_id'] = prop_id
        if listed_by:
            prop_details['listed_by'] = listed_by[0]
        if locality:
            prop_details['locality'] = locality[0]
        if city:
            prop_details['city'] = city[0]
        if name:
            prop_details['name'] = name[0]
        if address:
            prop_details['address'] = address[0]
        if rent:
            prop_details['rent'] = rent[0]
        if city:
            prop_details['deposit'] = deposit[0]
        if bhk:
            prop_details['bhk'] = bhk[0]
        if area:
            prop_details['area'] = area[0]
        if latitude:
            prop_details['latitude'] = latitude[0]
        if longitude:
            prop_details['longitude'] = longitude[0]
        if posted_date:
            prop_details['posted_date'] = posted_date[0]
        if description:
            prop_details['description'] = description[0]
        if note:
            prop_details['note'] = note[0]
        if magicbricks_verified:
            prop_details['magicbricks_verified'] = magicbricks_verified[0]
        if construction_age:
            prop_details['construction_age'] = construction_age[0]
        if society:
            prop_details['society'] = society[0]
        if project_url:
            prop_details['project_url'] = project_url[0]