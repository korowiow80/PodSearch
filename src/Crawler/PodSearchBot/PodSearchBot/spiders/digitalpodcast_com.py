from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector

from PodSearchBot.items import PodsearchbotItem

from Util.PathTool.PathTool import PathTool
from Resource.Resource import Resource


class Digitalpodcast_com(CrawlSpider):

    start_urls = ["http://www.digitalpodcast.com/opml/digitalpodcast.opml"]    # public for scrapy
    
    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = '../' + _url.getPath()                 # public for scrapy

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        #podcast_urls_xpath = "/opml/body/outline/outline/@url"
        podcast_urls_xpath = "//outline/@url"
        links = hxs.select(podcast_urls_xpath).extract()
        for link in links:
            if link.startswith('/'):
                link = self._baseUrl + link
            item = PodsearchbotItem()
            item['link'] = link
            yield item
