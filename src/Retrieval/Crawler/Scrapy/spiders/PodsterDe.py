from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem

from Resource.PathTool import PathTool
from Resource.Resource import Resource


class PodsterDe(BaseSpider):

    start_urls = ["http://podster.de/tag/system:all"]       # public for scrapy
    
    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = _url.getPath()                         # public for scrapy

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        next_page_xpath = "//tr/td[3]/a/@href"
        next_page_urls = hxs.select(next_page_xpath).extract()
        if not next_page_urls: return 
        next_page_url = next_page_urls[0]
        yield Request(next_page_url, callback=self.parse)
        
        podcast_page_xpath = "//table[@class='podcasts']//tr[2]/td[1]/a/@href"
        podcast_page_urls = hxs.select(podcast_page_xpath).extract()
        for podcast_page_url in podcast_page_urls:
            yield Request(podcast_page_url, callback=self.parse_podcast_page)

    def parse_podcast_page(self, response):
        hxs = HtmlXPathSelector(response)      
        item = PodcastFeedItem()

        podcast_title_xpath = "//div[@id='caption-header']/text()"
        podcast_title = hxs.select(podcast_title_xpath).extract()[0]
        podcast_title = podcast_title[len(u'\n                 '):]
        podcast_title = podcast_title[len("Podcast: "):]
        podcast_title = podcast_title.rstrip(' ')
        item['title'] = podcast_title

        try:
            podcast_url_xpath = "//div[@id='content']//a[5]/@href"
            link = hxs.select(podcast_url_xpath).extract()[0]
            if not link.startswith('/community/map;show=') and \
               not link.startswith('http://podster.de/view/'):
                item['link'] = link
        except IndexError:
            pass
        try:
            podcast_url_xpath = "//div[@id='content']//a[4]/@href"
            link = hxs.select(podcast_url_xpath).extract()[0]
            if not link.startswith('/community/map;show=') and \
               not link.startswith('http://podster.de/view/'):
                item['link'] = link
        except IndexError:
            pass
        try:
            podcast_url_xpath = "//div[@id='content']//div[@class='boxcontent']/a[2]/@href"
            link = hxs.select(podcast_url_xpath).extract()[0]            
            if not link.startswith('/community/map;show=') and \
               not link.startswith('http://podster.de/view/'):
                item['link'] = link
        except IndexError:
            pass
        try:
            link = item['link']
        except KeyError:
            print 'PodsterDe: WARNING: The page %s did not contain a link to a feed.' % response.url
            return

        yield item
