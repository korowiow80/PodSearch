import listparser
from scrapy.contrib.spiders import CrawlSpider

from PodSearchBot.items import PodsearchbotItem

from Util.PathTool.PathTool import PathTool
from Resource.Resource import Resource


class Bitlove_org(CrawlSpider):

    start_urls = ["http://bitlove.org/directory.opml"]      # public for scrapy
    
    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.get_base_url()
    name = _url.get_spider_name()                           # public for scrapy
    feed_list_path = '../' + _url.get_path()                # public for scrapy

    def parse(self, response):
        d = listparser.parse(response.body)
        feeds = d.feeds
        for feed in feeds:
            item = PodsearchbotItem()
            item['link'] = feed.url
            yield item
