import scrapy 
import pickle

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class MagicBricks(scrapy.Spider):

	name = "extract_cities"

	start_urls = ["http://www.magicbricks.com/property-for-sale-rent-in-Bangalore/residential-real-estate-Bangalore"]

	def parse(self, response):
		cities = response.xpath("//div[@class='w_20_per']/a/@href").extract()
		cities = [str(city) for city in cities]
		cities = [city[city.index("estate")+len("estate-"):] for city in cities]
		cities = ['Bangalore', 'Mumbai', 'Pune', 'Chennai', 'Hyderabad', 'Kolkata', 'Ahmedabad', 'Navi-Mumbai', 'Thane', 'Noida', 'Gurgaon', 'Ghaziabad', 'Faridabad', 'Greater-Noida', 'New-Delhi', 'Agra', 'Aurangabad', 'Bhiwadi', 'Bhopal', 'Bhubaneswar', 'Bokaro-Steel-City', 'Chandigarh', 'Coimbatore', 'Dehradun', 'Durgapur', 'Goa', 'Gorakhpur', 'Guntur', 'Guwahati', 'Haridwar', 'Indore', 'Jaipur', 'Jamshedpur', 'Jodhpur', 'Kanpur', 'Kochi', 'Kottayam', 'Kozhikode', 'Lucknow', 'Madurai', 'Mangalore', 'Manipal', 'Mysore', 'Nagpur', 'Nashik', 'Navsari', 'Palghar', 'Patna', 'Rajahmundry', 'Ranchi', 'Raipur', 'Salem', 'Surat', 'Thrissur', 'Trivandrum', 'Trichy', 'Udaipur', 'Udupi', 'Vadodara', 'Vapi', 'Varanasi', 'Vijayawada', 'Visakhapatnam', 'Vrindavan']
		save_obj(cities,'cities')