# Scrapy settings for Scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'Scrapy'
BOT_VERSION = '1.0'

ITEM_PIPELINES = [
    'Scrapy.pipelines.FeedListPipeline'
]

SPIDER_MODULES = ['Scrapy.spiders']
NEWSPIDER_MODULE = 'Scrapy.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
