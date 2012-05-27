# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter # TODO use JsonLinesItemExporter

class FeedListPipeline(object):

    def __init__ (self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        f = open(spider.feedListPath, 'w+b')
        self.files[spider] = f
        self.exporter = JsonItemExporter(f)
        self.exporter.start_exporting()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        f = self.files.pop(spider)
        f.close()
