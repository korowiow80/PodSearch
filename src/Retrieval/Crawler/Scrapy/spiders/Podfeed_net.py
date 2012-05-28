from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem

from PathTool import PathTool
from UrlTool import UrlTool


class Podfeed_net(BaseSpider):
    
    start_urls = ["http://www.podfeed.net/site_map.asp"]

    _ut = UrlTool()
    _pt = PathTool()

    _baseUrl = _ut.getBaseUrl(start_urls[0])
    name = _ut.getSpiderName(start_urls[0]) # needs to be public for scrapy
    feedListPath = _pt.getFeedListPath(start_urls[0])

    items = []

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sitemapPageXpath = "/html/body/div[@class='container']/div[@id='column']/a/@href"
        sitemapPageUrls = hxs.select(sitemapPageXpath).extract()
        for sitemapPageUrl in sitemapPageUrls:
            url = self._ut.getAbsoluteUrl(sitemapPageUrl, self._baseUrl)
            yield Request(url, callback=self.parse_sitemapPage)           

    def parse_sitemapPage(self, response):
        hxs = HtmlXPathSelector(response)
        podcastPageXpath = "/html/body/div[@class='container']/div[@id='column']/a/@href"
        podcastPageUrls = hxs.select(podcastPageXpath).extract()
        for podcastPageUrl in podcastPageUrls:
            yield Request(podcastPageUrl, callback=self.parse_podcastPage)

    def parse_podcastPage(self, response):
        hxs = HtmlXPathSelector(response)
        podcastTitleXpath = "/html/body/div[@class='container']/div[@id='column']/div[@id='podcast']/div[@id='podcast_details']/div[@class='content']/div[@class='konafilter']/h1/text()"
        podcastUrlXpath = "/html/body/div[@class='container']/div[@id='column']/div[@id='podcast']/div[@id='podcast_details']/div[@class='konafilter']/div[@class='pf_box_header right nomobile']/ul[@class='chicklets nomobile']/li[3]/a/@href"
        
        podcastTitle = hxs.select(podcastTitleXpath).extract()
        podcastLink = hxs.select(podcastUrlXpath).extract()
        if not podcastTitle or not podcastLink: return
        if podcastLink[0] == "#": return 
        item = PodcastFeedItem()
        item['title'] = podcastTitle[0]
        item['link'] = podcastLink[0]

        yield item