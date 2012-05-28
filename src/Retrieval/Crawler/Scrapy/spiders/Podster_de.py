from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem

from PathTool import PathTool
from UrlTool import UrlTool


class Podster_de(BaseSpider):

    start_urls = ["http://podster.de/tag/system:all"]
    
    _ut = UrlTool()
    _pt = PathTool()

    _baseUrl = _ut.getBaseUrl(start_urls[0])
    name = _ut.getSpiderName(start_urls[0]) # needs to be public for scrapy
    feedListPath = _pt.getFeedListPath(start_urls[0])

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        nextPageXpath = "//tr/td[3]/a/@href"
        nextPageUrls = hxs.select(nextPageXpath).extract()
        if not nextPageUrls: return 
        nextPageUrl = nextPageUrls[0]
        yield Request(nextPageUrl, callback=self.parse)
        
        podcastPageXpath = "//table[@class='podcasts']//tr[2]/td[1]/a/@href"
        podcastPageUrls = hxs.select(podcastPageXpath).extract()
        for podcastPageUrl in podcastPageUrls:
            yield Request(podcastPageUrl, callback=self.parse_podcastPage)

    def parse_podcastPage(self, response):
        hxs = HtmlXPathSelector(response)      
        item = PodcastFeedItem()

        podcastTitleXpath = "//div[@id='caption-header']/text()"
        podcastTitle = hxs.select(podcastTitleXpath).extract()[0]
        podcastTitle = podcastTitle[len(u'\n                 '):]
        podcastTitle = podcastTitle[len("Podcast: "):]
        podcastTitle = podcastTitle.rstrip(' ')
        item['title'] = podcastTitle

        try:
            podcastUrlXpath = "//div[@id='content']//a[5]/@href"
            link = hxs.select(podcastUrlXpath).extract()[0]
            if not link.startswith('/community/map;show=') and \
               not link.startswith('http://podster.de/view/'):
                item['link'] = link
        except IndexError:
            pass
        try:
            podcastUrlXpath = "//div[@id='content']//a[4]/@href"
            link = hxs.select(podcastUrlXpath).extract()[0]
            if not link.startswith('/community/map;show=') and \
               not link.startswith('http://podster.de/view/'):
                item['link'] = link
        except IndexError:
            pass
        try:
            podcastUrlXpath = "//div[@id='content']//div[@class='boxcontent']/a[2]/@href"
            link = hxs.select(podcastUrlXpath).extract()[0]            
            if not link.startswith('/community/map;show=') and \
               not link.startswith('http://podster.de/view/'):
                item['link'] = link
        except IndexError:
            pass
        try:
            link = item['link']
        except KeyError:
            print 'Podster_de: WARNING: The page %s did not contain a link to a feed.' % response.url
            return

        yield item