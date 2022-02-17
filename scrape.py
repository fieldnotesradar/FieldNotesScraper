from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    name = "sitemap"
    sitemap_urls = [
        'https://fieldnotesbrand.com/sitemaps-1-product-seasonalEditions-1-sitemap.xml',
        'https://fieldnotesbrand.com/sitemaps-1-product-memoBooks-1-sitemap.xml',
        'https://fieldnotesbrand.com/sitemaps-1-product-otherNotebooks-1-sitemap.xml'
    ]

    def parse(self, response):
        yield {
            'item': response.xpath('//*[@class="l-panel-header__left"]/span/text()').get(),
            'url': response.url,
            'title': response.xpath('//*[@class="panel__title"]/text()').get().strip(),
            'dimensions': response.xpath('//*[@class="panel__details"]/span/text()').get(),
            'subtitle': response.xpath('//*[@class="panel__sub-title"][1]/text()').get().strip(),
            'details': response.xpath('//*[@class="panel__sub-title"][2]/text()').get().strip(),
            'price': response.xpath('//meta[@property="product:price:amount"]/@content').get(),
            'id': response.xpath('//meta[@property="product:retailer_item_id"]/@content').get(),
            'availability': response.xpath('//meta[@property="product:availability"]/@content').get(),
        }