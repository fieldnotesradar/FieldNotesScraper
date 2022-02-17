from scrapy.spiders import SitemapSpider
from scrapy.http import Request

class MySpider(SitemapSpider):
    name = "sitemap"
    sitemap_urls = ['https://fieldnotesbrand.com/robots.txt']
    sitemap_rules = [
        ('/products/', 'parse'),
    ]

    other_urls = ['https://fieldnotesbrand.com/products/leap-of-faith']

    def start_requests(self):
        requests = list(super(MySpider, self).start_requests())
        requests += [Request(x, self.parse) for x in self.other_urls]
        return requests

    def parse(self, response):
        yield {
            'id': response.xpath('//meta[@property="product:retailer_item_id"]/@content').get(),
            'item': response.xpath('//*[@class="l-panel-header__left"]/span/text()').get(),
            'url': response.url,
            'title': response.xpath('//*[@class="panel__title"]/text()').get().strip(),
            'dimensions': response.xpath('//*[@class="panel__details"]/span/text()').get(),
            'subtitle': response.xpath('//*[@class="panel__sub-title"][1]/text()').get().strip(),
            'details': response.xpath('//*[@class="panel__sub-title"][2]/text()').get().strip(),
            'price': response.xpath('//meta[@property="product:price:amount"]/@content').get(),
            'availability': response.xpath('//meta[@property="product:availability"]/@content').get(),
        }