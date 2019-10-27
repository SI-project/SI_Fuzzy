from scrapy import Spider, Selector, Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider

class WikiSpider(Spider):
    name = "WikiSpider"
    start_urls = [
        'http://en.wikipedia.org/',
    ]
    allowed_domains = [
        'en.wikipedia.org',
    ]
    avoids = [
        "https://en.wikipedia.org/w/index.php",
        "https://en.m.wikipedia.org/",
        "https://en.wikipedia.org/w/api.php",
    ]
    rules = (
        Rule(LinkExtractor(allow="https://en.wikipedia.org/", deny=avoids), callback='parse', follow=True),
    )
    custom_settings = {
        'DEPTH_PRIORITY': 1,
    }

    def __init__(self, topic='Marvel'):
        super(WikiSpider, self).__init__()
        self.start_urls = ['https://www.wikipedia.org/wiki/%s' % topic]
        self.max_count = 0

    def parse(self, response):
        resp = Selector(response)
        title = resp.xpath('//title//text()').extract_first()

        text = ' '.join(resp.xpath("//body//text()").extract())

        self.max_count += 1
        yield {"{}---{}".format(title,response.url):text}
        new_links = []

        links = resp.xpath('//a/@href').extract()
        for l in links:
            if "#" == l[0]:
                continue
            if "http:" in l:
                new_links.append(l)
            else:
                new_links.append(response.urljoin(l))

        if self.max_count >= 100:
            raise CloseSpider("End with {} pages".format(self.max_count))
        for next_page in new_links:
            yield Request(url=next_page, callback=self.parse)