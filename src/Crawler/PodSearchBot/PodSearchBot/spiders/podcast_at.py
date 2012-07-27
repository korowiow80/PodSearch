import exceptions
import httplib

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import httplib2

from PodSearchBot.items import PodsearchbotItem

from Util.PathTool.PathTool import PathTool
from Resource.Resource import Resource
import socket


class Podcast_at(CrawlSpider):

    start_urls = ["http://www.podcast.at/podcasts.html"]    # public for scrapy
    
    _pt = PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = '../' + _url.getPath()                 # public for scrapy

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        next_page_xpath = "/html/body/div[@class='container_20']/div[@class='container_20']/div[@id='middle']/div[@id='podcasts_home']/div[@class='browseteaser_full']/div[@class='inner']/div[@class='page_select']/a[@class='podcast_browse'][5]/@href"
        next_page_urls = hxs.select(next_page_xpath).extract()
        if not next_page_urls: return
        next_page_url = next_page_urls[0]
        if next_page_url.startswith('/'):
            next_page_url = self._baseUrl + next_page_url
        yield Request(next_page_url, callback=self.parse)
        
        podcast_page_xpath = "/html/body/div[@class='container_20']/div[@class='container_20']/div[@id='middle']/div[@id='podcasts_home']/div[@class='browseteaser_full']/div[@class='inner']/div[@class='podcast_listing_box']/div/div[@class='podcast_listing_content']/a/@href"
        podcast_page_urls = hxs.select(podcast_page_xpath).extract()
        for podcast_page_url in podcast_page_urls:
            if podcast_page_url.startswith('/'):
                podcast_page_url = self._baseUrl + podcast_page_url
            yield Request(podcast_page_url, callback=self.parse_podcast_page)

    def parse_podcast_page(self, response):
        hxs = HtmlXPathSelector(response)      
        item = PodsearchbotItem()

        podcast_url_xpath = "/html/body/div[@class='container_20']/div[@id='teasertitle']/div[@class='teasertitle']/a/@href"
        link = hxs.select(podcast_url_xpath).extract()[0]
        if link.startswith('/'):
            link = self._baseUrl + link
        if link.startswith(self._baseUrl + '/podcast_url'):
            try:
                link = self.getContentLocation(link)
            except exceptions.KeyError:
                # broken link
                pass # return
        item['link'] = link
        yield item

    def getContentLocation(self, link):
        try:
            cacheDir = ".cache"
            timeoutSecs = 5
            h = httplib2.Http(cacheDir, timeoutSecs, disable_ssl_certificate_validation=True)
            h.follow_all_redirects = True
            resp = h.request(link, "GET")[0]
            contentLocation = resp['content-location']
        except (exceptions.TypeError, socket.error, socket.timeout, httplib.BadStatusLine, httplib2.RelativeURIError, httplib2.ServerNotFoundError):
            return link
        return contentLocation
