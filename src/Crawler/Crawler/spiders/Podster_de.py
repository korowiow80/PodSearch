import re

from scrapy.spider import BaseSpider
from scrapy.utils.response import body_or_str
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import os
import errno

import tldextract

import Crawler.items

class Podster_de(BaseSpider):
    start_urls = ["http://podster.de/tag/system:all"]
    
    # extract fullDomain from URL
    extract = tldextract.extract(start_urls[0])
    if extract.subdomain:
        fullDomain = ".".join(extract)
        domainTld = ".".join(extract[1:])
    else:
        fullDomain = ".".join(extract[1:])
        domainTld = None
    
    # derive name from TLD
    # by general convention the first letter of a class gets capitalized
    # by our convention, we skip the sub-domain, if it is 'www'
    if domainTld:
        name = domainTld[0].upper() + domainTld.replace('.', '_')[1:]
    else:
        name = fullDomain[0].upper() + fullDomain.replace('.', '_')[1:]

    # derive prefix from domain
    # by convention we skip the www
    if domainTld:
        prefix = "../../static/0-Directories/" + domainTld + "/"
    else:
        prefix = "../../static/0-Directories/" + fullDomain + "/"

    # make sure the prefix exists
    try:
        os.makedirs(prefix)
    except OSError as exc:
        if exc.errno == errno.EEXIST: pass
        else: raise
        
    def parse(self, response):        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" %(nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_page)
            break

    def parse_page(self, response):
        filename = self.prefix + response.url.split("/")[-1:][0]
        open(filename, 'wb').write(response.body)
        
        text = body_or_str(response)

        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" %(nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            yield Request(url, callback=self.parse_podcast)
            break

    def parse_podcast(self, response):
        filename = self.prefix + response.url.split("/")[-1:][0]
        open(filename, 'wb').write(response.body)
        
        hxs = HtmlXPathSelector(response)

        item = Crawler.items.PodcastFeedItem()
        item['title'] = hxs.select("/html/body/div[@id='wrap']/div[@id='bodyarea']/div[@id='body_left']/div[@id='most_popular_podcast']/div[@class='mod-100 clear pbl mbl brdrBottom']/div[@class='mod-80']/h2[@class='txtGreen mtn']/text()").extract()[0]
        item['link'] = 'Podcast.com does not offer links'
        
        yield item