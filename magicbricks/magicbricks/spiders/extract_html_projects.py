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

    name = 'extract_html_projects'

    def start_requests(self):
        for root, dirs, files in os.walk('obj/city_urls_projects/'):
            for file in files:
                city = re.sub('.txt','',file)

                if not os.path.exists('html/projects_html/'+city):
                    os.makedirs('html/projects_html/'+city)
                f = open ('obj/city_urls_projects/'+file,'r')
                for line in f:
                    url = 'https://www.magicbricks.com' + line
                    yield scrapy.Request(url=url,callback=self.parse,meta={'city':city})

    def parse(self, response):
        if response.status!= 200:
            file = 'html/projects_html/failed.txt' 
            with open(file, 'a') as f:
                f.write(response.url)
                f.write("\n")

        p_id = response.url
        p_id=p_id[p_id.index("pdpid")+len("pdpid-"):]
        file = 'html/projects_html/%s/%s' % (response.meta['city'], p_id)
        with open(file, 'w') as f:
            f.write(response.body)
