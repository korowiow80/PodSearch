import re

from scrapy.spider import BaseSpider
from scrapy.utils.response import body_or_str
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from Scrapy.items import PodcastFeedItem
from Scrapy.spiders import SpiderTool

class Podcast_com(BaseSpider):
    start_urls = ["http://www.podcast.com/sitemap.xml"]

    st = SpiderTool.SpiderTool()
    baseUrl, feedListFile, name, prefix = SpiderTool.SpiderTool().derive(start_urls[0])

    def parse(self, response):        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" %(nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_sitemapPage)
            break

    def parse_sitemapPage(self, response):
        filename = self.prefix + response.url.split("/")[-1:][0]
        open(filename, 'wb').write(response.body)
        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" %(nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_podcastPage)
            break

    def parse_podcastPage(self, response):
        filename = self.prefix + response.url.split("/")[-1:][0]
        open(filename, 'wb').write(response.body)
        
        hxs = HtmlXPathSelector(response)

        item = PodcastFeedItem()
        item['title'] = hxs.select("/html/body/div[@id='wrap']/div[@id='bodyarea']/div[@id='body_left']/div[@id='most_popular_podcast']/div[@class='mod-100 clear pbl mbl brdrBottom']/div[@class='mod-80']/h2[@class='txtGreen mtn']/text()").extract()[0]
        item['link'] = 'Podcast.com does not offer links'
        
        yield item