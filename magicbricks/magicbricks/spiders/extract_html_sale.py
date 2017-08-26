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

    name = 'extract_html_sale'

    def start_requests(self):
        #for root, dirs, files in os.walk('obj/city_urls_sale/urls_sale_apartment/'):
        files = ['Pune.txt',  'Hyderabad.txt', 'Kolkata.txt', 'Navi-Mumbai.txt', 'Thane.txt', 'Noida.txt', 'Gurgaon.txt', 'Ghaziabad.txt', 'Faridabad.txt', 'Greater-Noida.txt', 'New-Delhi.txt', 'Coimbatore.txt', 'Dehradun.txt', 'Durgapur.txt', 'Goa.txt', 'Gorakhpur.txt', 'Guntur.txt', 'Guwahati.txt', 'Haridwar.txt', 'Indore.txt', 'Jaipur.txt', 'Jamshedpur.txt', 'Jodhpur.txt', 'Kanpur.txt', 'Kochi.txt', 'Kottayam.txt', 'Kozhikode.txt', 'Lucknow.txt', 'Madurai.txt', 'Mangalore.txt', 'Manipal.txt', 'Mysore.txt', 'Nagpur.txt', 'Nashik.txt', 'Navsari.txt', 'Palghar.txt', 'Patna.txt', 'Rajahmundry.txt', 'Ranchi.txt', 'Raipur.txt', 'Salem.txt', 'Surat.txt', 'Thrissur.txt', 'Trivandrum.txt', 'Trichy.txt', 'Udaipur.txt', 'Udupi.txt', 'Vadodara.txt', 'Vapi.txt', 'Varanasi.txt', 'Vijayawada.txt', 'Visakhapatnam.txt', 'Vrindavan.txt']
        for file in files:
            city = re.sub('.txt','',file)
            if not os.path.exists('html/sale_html/apartment/'+city):
                os.makedirs('html/sale_html/apartment/'+city)
            f = open ('obj/city_urls_sale/urls_sale_apartment/'+file,'r')
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
        p_id = p_id[p_id.index("id=")+len("id="):]
        file = 'html/sale_html/apartment/%s/%s' % (response.meta['city'], p_id)
        with open(file, 'w') as f:
            f.write(response.body)