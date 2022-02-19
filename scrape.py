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
        for entry in entries:
            if hasattr(self, 'minutes'):
                lastmod = arrow.get(entry['lastmod']).to('utc')
                if (arrow.utcnow() - lastmod) <= timedelta(minutes=int(self.minutes)):
                    yield entry
            else:
                yield entry

    def parse_product(self, response):
        yield {
            response.url: {
                'type': 'product',
                'id': response.xpath('//meta[@property="product:retailer_item_id"]/@content').get(),
                'item': response.xpath('//*[@class="l-panel-header__left"]/span/text()').get(),
                'title': response.xpath('//*[@class="panel__title"]/text()').get().strip(),
                'price': response.xpath('//meta[@property="product:price:amount"]/@content').get(),
                'availability': response.xpath('//meta[@property="product:availability"]/@content').get(),
            }
        }
    
    def parse_film(self, response):
        yield {
            response.url: {
                'type': 'film',
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
                'category': response.xpath('//*[@class="blog-post__header"]/h2/a/text()').get(),
                'title': response.xpath('//*[@class="blog-post__header"]/h1/text()').get(),
                'date': response.xpath('//*[@class="blog-post__header"]/h3/text()').get(),
            }
        }