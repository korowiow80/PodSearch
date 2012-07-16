from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem

from Resource.Resource import Resource
from Resource.PathTool import PathTool


class PodfeedNet(BaseSpider):
    
    start_urls = ["http://www.podfeed.net/site_map.asp"]    # public for scrapy

    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = _url.getPath()                         # public for scrapy

    items = []

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sitemap_page_xpath = "/html/body/div[@class='container']/div[@id='column']/a/@href"
        sitemap_page_urls = hxs.select(sitemap_page_xpath).extract()
        for sitemap_page_url in sitemap_page_urls:
            resource = Resource(self._baseUrl + sitemap_page_url, "directory")
            url = resource.getAbsoluteUrl()
            yield Request(url, callback=self.parse_sitemap_page)           

    def parse_sitemap_page(self, response):
        hxs = HtmlXPathSelector(response)
        podcast_page_xpath = "/html/body/div[@class='container']/div[@id='column']/a/@href"
        podcast_page_urls = hxs.select(podcast_page_xpath).extract()
        for podcast_page_url in podcast_page_urls:
            yield Request(podcast_page_url, callback=self.parse_podcast_page)

    def parse_podcast_page(self, response):
        hxs = HtmlXPathSelector(response)
        podcast_url_xpath = "/html/body/div[@class='container']/div[@id='column']/div[@id='podcast']/div[@id='podcast_details']/div[@class='konafilter']/div[@class='pf_box_header right nomobile']/ul[@class='chicklets nomobile']/li[3]/a/@href"
        
        podcast_link = hxs.select(podcast_url_xpath).extract()
        if not podcast_link:
            return
        if podcast_link[0] == "#":
            return 
        item = PodcastFeedItem()
        item['link'] = podcast_link[0]
        yield item
