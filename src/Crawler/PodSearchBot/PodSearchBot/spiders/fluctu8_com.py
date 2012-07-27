import exceptions

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request

from PodSearchBot.items import PodsearchbotItem
from Resource.Resource import Resource
from Util.PathTool.PathTool import PathTool


class Fluctu8_com(CrawlSpider):
    allowed_domains = ['fluctu8.com']                       # public for scrapy
    start_urls = [                                          # public for scrapy
                  'http://www.fluctu8.com/sitemap/index-map-0.html',
                  'http://www.fluctu8.com/sitemap/index-map-1.html',
                  'http://www.fluctu8.com/sitemap/index-map-2.html',
                  'http://www.fluctu8.com/sitemap/index-map-3.html',
                  'http://www.fluctu8.com/sitemap/index-map-4.html',
                  'http://www.fluctu8.com/sitemap/index-map-5.html',
                  'http://www.fluctu8.com/sitemap/index-map-6.html',
                  'http://www.fluctu8.com/sitemap/index-map-7.html',
                  'http://www.fluctu8.com/sitemap/index-map-8.html',
                  'http://www.fluctu8.com/sitemap/index-map-9.html']
    
    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = '../' + _url.getPath()                 # public for scrapy

    links = []

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sitemap_page_xpath = "/html/body/a/@href"
        sitemap_page_urls = hxs.select(sitemap_page_xpath).extract()
        for sitemap_page_url in sitemap_page_urls:
            resource = Resource(self._baseUrl + sitemap_page_url, "directory")
            url = resource.getAbsoluteUrl()
            yield Request(url, callback=self.parse_sitemap_page)

    def parse_sitemap_page(self, response):
        hxs = HtmlXPathSelector(response)
        podcast_page_xpath = "/html/body/a/@href"
        podcast_page_urls = hxs.select(podcast_page_xpath).extract()
        for podcast_page_url in podcast_page_urls:
            if podcast_page_url.startswith('/'):
                podcast_page_url = self._baseUrl + podcast_page_url
            yield Request(podcast_page_url, callback=self.parse_podcast_page)

    def parse_podcast_page(self, response):
        hxs = HtmlXPathSelector(response)
        podcast_url_xpath = "//table[@class='entry']//tr[1]/td/a[1]/@href"
        podcast_link = hxs.select(podcast_url_xpath).extract()
        try:
            item = PodsearchbotItem()
            item['link'] = podcast_link[1]
        except exceptions.IndexError:
            return
        yield item
