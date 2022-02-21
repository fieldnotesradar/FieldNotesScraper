import hashlib
from scrapy.spiders import SitemapSpider
from scrapy.http import Request
from datetime import timedelta
import arrow

class MySpider(SitemapSpider):
    name = "sitemap"
    sitemap_urls = ['https://fieldnotesbrand.com/robots.txt']
    sitemap_rules = [
        ('/products/', 'parse_product'),
        ('/films/', 'parse_film'),
        ('/dispatches/', 'parse_dispatch'),
    ]
    
    other_product_urls = ['https://fieldnotesbrand.com/products/leap-of-faith']

    def start_requests(self):
        requests = list(super(MySpider, self).start_requests())
        requests += [Request(x, self.parse_product) for x in self.other_product_urls]
        return requests

    def sitemap_filter(self, entries):
        minutes = getattr(self, 'minutes', None)
        for entry in entries:
            if minutes:
                lastmod = arrow.get(entry['lastmod']).to('utc')
                if (arrow.utcnow() - lastmod) <= timedelta(minutes=int(minutes)):
                    yield entry
            else:
                yield entry

    def parse_product(self, response):
        yield {
            response.url: {
                'type': 'product',
                'id': response.url.split("/")[-1],
                'contentHash': hashlib.md5(''.join(response.xpath('//*[contains(@class, "rich-text")]/p/text()').extract()).encode('utf-8')).hexdigest(),
                'retailerItemId': response.xpath('//meta[@property="product:retailer_item_id"]/@content').get(),
                'code': response.xpath('//*[@class="l-panel-header__left"]/span/text()').get(),
                'title': (response.xpath('//*[@class="panel__title"]/text()').get() or "").strip(),
                'dimensions': response.xpath('//*[@class="panel__details"]/span/text()').get(),
                'subtitle': (response.xpath('//*[@class="panel__sub-title"][1]/text()').get() or "").strip(),
                'details': (response.xpath('//*[@class="panel__sub-title"][2]/text()').get() or "").strip(),
                'price': response.xpath('//meta[@property="product:price:amount"]/@content').get(),
                'availability': response.xpath('//meta[@property="product:availability"]/@content').get(),
            }
        }
    
    def parse_film(self, response):
        yield {
            response.url: {
                'type': 'film',
                'id': response.url.split("/")[-1],
                'title': response.xpath('//meta[@property="og:title"]/@content').get(),
                'video_url': response.xpath('//*[@class="film-teaser__text"]/a/@href').get(),
                'teaser_link': response.xpath('//*[@class="film-teaser__link"]/@href').get(),
                'teaser_text': response.xpath('//*[@class="film-teaser__text"]/p/text()').get(),
            }
        }

    def parse_dispatch(self, response):
        yield {
            response.url: {
                'type': 'dispatch',
                'id': response.url.split("/")[-1],
                'contentHash': hashlib.md5(''.join(response.xpath('//*[contains(@class, "rich-text")]/p/text()').extract()).encode('utf-8')).hexdigest(),
                'category': response.xpath('//*[@class="blog-post__header"]/h2/a/text()').get(),
                'title': response.xpath('//*[@class="blog-post__header"]/h1/text()').get(),
                'date': response.xpath('//*[@class="blog-post__header"]/h3/text()').get(),
            }
        }