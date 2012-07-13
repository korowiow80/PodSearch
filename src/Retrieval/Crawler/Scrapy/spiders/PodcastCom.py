import re

from scrapy.spider import BaseSpider
from scrapy.utils.response import body_or_str
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem

from Resource.PathTool import PathTool
from Resource.Resource import Resource


class PodcastCom(BaseSpider):
    
    start_urls = ["http://www.podcast.com/sitemap.xml"]     # public for scrapy

    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = _url.getPath()                         # public for scrapy

    def parse(self, response):        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_sitemap_page)
            break

    def parse_sitemap_page(self, response):       
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_podcast_page)
            break

    def parse_podcast_page(self, response):
        hxs = HtmlXPathSelector(response)

        item = PodcastFeedItem()
        item['title'] = hxs.select("/html/body/div[@id='wrap']/div[@id='bodyarea']/div[@id='body_left']/div[@id='most_popular_podcast']/div[@class='mod-100 clear pbl mbl brdrBottom']/div[@class='mod-80']/h2[@class='txtGreen mtn']/text()").extract()[0]
        item['link'] = 'Podcast.com does not offer links'
        
        yield item
