from scrapy.contrib.spiders import CrawlSpider
import listparser

from PodSearchBot.items import PodsearchbotItem

from Util.PathTool.PathTool import PathTool
from Resource.Resource import Resource


class Bitlove_org(CrawlSpider):

    start_urls = ["http://bitlove.org/directory.opml"]    # public for scrapy
    
    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = '../' + _url.getPath()                 # public for scrapy

    def parse(self, response):
        d = listparser.parse(response.body)
        feeds = d.feeds
        for feed in feeds:
            item = PodsearchbotItem()
            item['link'] = feed.url
            yield item
