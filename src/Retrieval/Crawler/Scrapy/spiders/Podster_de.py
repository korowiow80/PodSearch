import re

from scrapy.spider import BaseSpider
from scrapy.utils.response import body_or_str
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem
from Scrapy.spiders import SpiderTool

class Podster_de(BaseSpider):
    urls = ["http://podster.de/tag/system:all"]
    
    st = SpiderTool.SpiderTool()
    name, prefix = st.derive(urls[0])        

    def parse(self, response):        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" %(nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_page)
            break

    def parse_page(self, response):
        filename = self.prefix + response.url.split("/")[-1:][0]
        open(filename, 'wb').write(response.body)
        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" %(nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_podcast)
            break

    def parse_podcast(self, response):
        filename = self.prefix + response.url.split("/")[-1:][0]
        open(filename, 'wb').write(response.body)
        
        hxs = HtmlXPathSelector(response)

        item = PodcastFeedItem()
        item['title'] = hxs.select("/html/body/div[@id='wrap']/div[@id='bodyarea']/div[@id='body_left']/div[@id='most_popular_podcast']/div[@class='mod-100 clear pbl mbl brdrBottom']/div[@class='mod-80']/h2[@class='txtGreen mtn']/text()").extract()[0]
        item['link'] = 'Podcast.com does not offer links'
        
        yield item