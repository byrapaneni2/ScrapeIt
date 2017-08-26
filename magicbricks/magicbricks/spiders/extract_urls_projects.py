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

	name = "extract_urls_projects"

	def start_requests(self):
		cities = load_obj('cities')
		for city in cities:
			url = "https://www.magicbricks.com/Real-estate-projects-search/ALL-RESIDENTIAL-new-project-%s/Page-1" % city
			yield scrapy.Request(url=url, callback=self.parse, meta={'city': city, 'page_num':1, 'urls':[]})
	def parse(self, response):
		page_num = response.meta['page_num']
		city = response.meta['city']
		urls = response.xpath("//div[@class='proNameColm1']/a/@href").extract()
		urls = list(set(urls))
		file = 'obj/city_urls_projects/%s.txt' % city
		with open(file, 'a') as f:
			for url in urls:
				f.write(url)
				f.write("\n")
		if page_num == 1:
			max_page_num = response.xpath("//span[@id='pageCount']/text()").extract()[0]
			max_page_num = max_page_num.decode('utf-8')
			max_page_num = int(float(max_page_num))
			for page_num in range(2,max_page_num+1):
				req_url = "https://www.magicbricks.com/Real-estate-projects-search/ALL-RESIDENTIAL-new-project-%s/Page-%d" % (city,page_num)
				yield scrapy.Request(url=req_url,callback=self.parse, meta={'city':city,'page_num':page_num})