# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import os
import exceptions

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class PodsearchbotPipeline(object):
    def __init__ (self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.links = []

    def spider_opened(self, spider):
        try:
            with open(spider.feed_list_path, 'r') as f:
                self.links = list(set(f.readlines()))
            # strip newlines, see:  http://stackoverflow.com/a/3849519/906658
            self.links = map(lambda s: s.strip(), self.links)
            # empty file
            open(spider.feed_list_path, 'w').close()
        except exceptions.IOError:
            # initial run with empty list of feeds
            pass
        
    def process_item(self, item, spider):
        link = item['link']
        if link in self.links:
            return link
        self.links.append(link)
        self.links.sort()
        self.write(spider.feed_list_path)
        return item
    
    def spider_closed(self, spider):
        self.write(spider.feed_list_path)
        #pass

    def write(self, feed_list_path):
        # empty file
        open(feed_list_path, 'w').close()
        # write feedlist to file 
        with open(feed_list_path, 'w') as f:
            for linkToWrite in self.links:
                f.write(linkToWrite.encode('utf-8') + os.linesep)
