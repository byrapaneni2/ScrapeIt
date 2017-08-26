from scrapy.spiders import SitemapSpider

class MagicBricks(SitemapSpider):
    name = 'test'
    sitemap_urls = ['https://www.magicbricks.com/sitemap_index.xml']

    def parse(self, response):
        yield {
            'title': response.css("title ::text").extract_first(),
            'url': response.url
        }