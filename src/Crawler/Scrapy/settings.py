# Scrapy settings for Scrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'PodSearchBot'
BOT_VERSION = '1.0'

DOWNLOADER_MIDDLEWARES = {
    ' scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware':543,
}
DNSCACHE_ENABLED = True

EXTENSIONS = {
      'scrapy.contrib.logstats.LogStats':500,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = ".scrapyCache"
HTTPCACHE_IGNORE_MISSING = True

ITEM_PIPELINES = ['Crawler.Scrapy.pipelines.FeedListPipeline']

NEWSPIDER_MODULE = 'Crawler.Scrapy.spiders'

SPIDER_MODULES = ['Crawler.Scrapy.spiders']

USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
