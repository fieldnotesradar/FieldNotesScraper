from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
    name = "sitemap"
    sitemap_urls = [
    'https://fieldnotesbrand.com/sitemaps-1-product-seasonalEditions-1-sitemap.xml',
    'https://fieldnotesbrand.com/sitemaps-1-product-memoBooks-1-sitemap.xml',
    'https://fieldnotesbrand.com/sitemaps-1-product-otherNotebooks-1-sitemap.xml'
    ]

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'products/{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')