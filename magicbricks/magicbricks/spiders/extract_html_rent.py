import scrapy
import pickle
import os
import re

def save_obj(obj, name):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name, 'rb') as f:
        return pickle.load(f)

class MagicBricks(scrapy.Spider):

    name = 'extract_html_rent'

    def start_requests(self):
        for root, dirs, files in os.walk('obj/city_urls_rent/urls_rent_villa/'):
            for file in files:
                city = re.sub('.txt','',file)

                if not os.path.exists('html/rent_html/villa/'+city):
                    os.makedirs('html/rent_html/villa/'+city)
                f = open ('obj/city_urls_rent/urls_rent_villa/'+file,'r')
                for line in f:
                    url = 'https://www.magicbricks.com' + line
                    yield scrapy.Request(url=url,callback=self.parse,meta={'city':city})

    def parse(self, response):
        if response.status!= 200:
            file = 'html/rent_html/failed.txt' 
            with open(file, 'a') as f:
                f.write(response.url)
                f.write("\n")

        p_id = response.url
        p_id = p_id[p_id.index("id=")+len("id="):]
        file = 'html/rent_html/villa/%s/%s' % (response.meta['city'], p_id)
        with open(file, 'w') as f:
            f.write(response.body)