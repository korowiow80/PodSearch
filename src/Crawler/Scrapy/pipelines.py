# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html


class FeedListPipeline(object):

    def __init__ (self):
        pass

    def spider_opened(self, spider):
        pass
    
    def process_item(self, item, spider):
        pass
    
    def spider_closed(self, spider):
        pass
