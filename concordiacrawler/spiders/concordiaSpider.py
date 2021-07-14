from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import IGNORED_EXTENSIONS

from concordiacrawler.items import ConcordiacrawlerItem

CUSTOM_IGNORED_EXTENSIONS = IGNORED_EXTENSIONS.copy()
CUSTOM_IGNORED_EXTENSIONS.append('php')


class ConcordiaSpider(CrawlSpider):
    name = 'concordia'
    allowed_domains = ['www.concordia.ca']
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'ROBOTSTXT_OBEY': True,
        'CLOSESPIDER_TIMEOUT': 1800,
        'CONCURRENT_REQUESTS': 256,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 256,
        'CONCURRENT_REQUESTS_PER_IP': 256,
        'Accept-Language': 'en'
    }

    start_urls = ['https://www.concordia.ca']
    rules = (
        Rule(LinkExtractor(allow_domains="www.concordia.ca",
                           deny_extensions=CUSTOM_IGNORED_EXTENSIONS,
                           allow=(),
                           deny=('.*/fr.html', '.*/fr/.+', '.*/zh.html', '.*/zh/.+', '.*/maps/.+', '.*.pdf')),
             callback="parse_items", follow=True),
    )

    def parse_items(self, response):
        # print(f"Existing settings: {self.settings.attributes.items()}")

        soup = BeautifulSoup(response.text, 'lxml')

        cnts = soup.find(id='content-main')
        if cnts:
            content = ''
            tags = ['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'th', 'td']

            for tag in tags:
                texts = cnts.find_all(tag)
                for txt in texts:
                    content += txt.text + '\n'
            content = content.replace(u'\xa0', u' ')
            content = content.replace(u'\u202f', u'')

            item = ConcordiacrawlerItem()
            item['url'] = response.url
            item['content'] = content
            yield item

            # link = LinkExtractor(deny_extensions=CUSTOM_IGNORED_EXTENSIONS,
            #                      deny=('.*/fr.html', '.*/fr/.+', '.*/maps/.+',r'/.pdf/'),
            #                      allow_domains='www.concordia.ca')
            # links = link.extract_links(response)
            # for link in links:
            #     yield Request(url=link.url, callback=self.parse_items)

    # def parse_details(self, response):
    #     item = response.meta.get('item', None)
    #     if item:
    #         return item
    #     else:
    #         self.log('No item received for %s' % response.url, level=log.WARNING)
