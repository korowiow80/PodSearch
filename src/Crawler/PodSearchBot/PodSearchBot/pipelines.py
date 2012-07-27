# -*- coding: utf-8 -*-
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
        self.changeCounter = 0

    def spider_opened(self, spider):
        try:
            with open(spider.feed_list_path, 'r') as f:
                self.links = list(set(f.readlines()))
            # strip newlines, see:  http://stackoverflow.com/a/3849519/906658
            self.links = map(lambda s: self.removeNonAscii(s.strip()), self.links)
            # empty file
            open(spider.feed_list_path, 'w').close()
        except exceptions.IOError:
            # initial run with empty list of feeds
            pass
        
    def process_item(self, item, spider):
        link = item['link']
        if link in self.links:
            return link
        self.changeCounter += 1
        self.links.append(link)
        self.links.sort()
        if self.changeCounter == 100: # or time_since_last_flush >= 30
            self.flush_pipeline(spider.feed_list_path)
            self.changeCounter = 0
        return item
    
    def spider_closed(self, spider):
        self.flush_pipeline(spider.feed_list_path)
        #pass

    def flush_pipeline(self, feed_list_path):
        # empty file
        open(feed_list_path, 'w').close()
        # flush_pipeline feedlist to file 
        with open(feed_list_path, 'w') as f:
            for linkToWrite in self.links:
                f.write(linkToWrite.encode('utf-8') + os.linesep)

    def removeNonAscii(self, s):
        return "".join(i for i in s if ord(i) < 128)

