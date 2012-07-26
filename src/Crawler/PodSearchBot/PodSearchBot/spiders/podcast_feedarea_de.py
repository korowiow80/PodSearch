import exceptions

import httplib2
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from PodSearchBot.items import PodsearchbotItem
from PathTool import PathTool
from Resource.Resource import Resource


class Podcast_feedarea_de(CrawlSpider):

    start_urls = ["http://podcast.feedarea.de/latest_podcasts_1.html"]    # public for scrapy
    
    _pt = PathTool.PathTool()

    _url = Resource(start_urls[0], "directory")
    _baseUrl = _url.getBaseUrl()
    name = _url.getSpiderName()                             # public for scrapy
    feed_list_path = '../' + _url.getPath()                 # public for scrapy

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        next_page_xpath = "/html/body/div[@id='page']/div[@id='content_home']/div[@id='podcast_catalog_teaser_col']/div[@id='podcast_teaser_2col']/div[@id='pagenavi_2col'][2]/center/a[@class='page_browse'][5]/@href"
        next_page_urls = hxs.select(next_page_xpath).extract()
        if not next_page_urls: return
        next_page_url = next_page_urls[0]
        if next_page_url.startswith('/'):
            next_page_url = self._baseUrl + next_page_url
        yield Request(next_page_url, callback=self.parse)
        
        #podcast_page_xpath = "/html/body/div[@id='page']/div[@id='content_home']/div[@id='podcast_catalog_teaser_col']/div[@id='podcast_teaser_2col']/div[@id='podcast_teaser_2col_content']/table/tbody/tr[2]/td[@class='toppodcast_content_odd']/a[@class='feedurl']/@href"
        podcast_page_xpath = "//a[@class='feedurl']/@href"
        podcast_page_urls = hxs.select(podcast_page_xpath).extract()
        for podcast_page_url in podcast_page_urls:
            if podcast_page_url.startswith('/'):
                podcast_page_url = self._baseUrl + podcast_page_url
            yield Request(podcast_page_url, callback=self.parse_podcast_page)

    def parse_podcast_page(self, response):
        hxs = HtmlXPathSelector(response)      
        item = PodsearchbotItem()

        podcast_url_xpath = "//td[@class='feed_headbox'][1]/h1[@class='feed_head']/a/@href"
        link = hxs.select(podcast_url_xpath).extract()[0]
        if link.startswith('/'):
            link = self._baseUrl + link
        if link.startswith(self._baseUrl + '/feed_url'):
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
        except httplib2.ServerNotFoundError:
            # httplib2 was unable to find the server
            return link
        return contentLocation
