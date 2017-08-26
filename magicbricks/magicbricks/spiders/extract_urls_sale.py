import scrapy 
import pickle
import re
import json

def save_obj(obj, name):
    with open('obj/city_urls'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f,pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class MagicBricks(scrapy.Spider):

	name = "extract_sale_urls"

	def start_requests(self):
		cities = load_obj('cities')
		for city in cities:
			url = "http://www.magicbricks.com/property-for-sale/ALL-RESIDENTIAL-real-estate-%s/Page-1" % city
			yield scrapy.Request(url=url, callback=self.parse, meta={'city': city, 'page_num':1, 'urls':[]})
	def parse(self, response):
		page_num = response.meta['page_num']
		city = response.meta['city']
		urls = response.xpath("//div[@class='proBrf']//a[@class='property-sticky-link']/@href").extract()
		#urls = list(set(urls))
		file = 'obj/city_urls_sale/%s.txt' % city
		with open(file, 'a') as f:
			for url in urls:
				f.write(url)
				f.write("\n")
		if page_num == 1:
			max_page_num = response.xpath("//span[@class='pageNos']//a[@class='act']/b/text()").extract()[-1]
			max_page_num = int(max_page_num)
			for page_num in range(2,max_page_num+1):
				req_url= "http://www.magicbricks.com/property-for-sale/ALL-RESIDENTIAL-real-estate-%s/Page-%d" % (city,page_num)
				yield scrapy.Request(url=req_url,callback=self.parse, meta={'city':city,'page_num':page_num})