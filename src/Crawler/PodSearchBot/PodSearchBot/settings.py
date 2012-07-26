# Scrapy settings for PodSearchBot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'PodSearchBot'
BOT_VERSION = '1.0'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware':543,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_DIR = ".scrapyCache"
HTTPCACHE_IGNORE_MISSING = False

ITEM_PIPELINES = ['PodSearchBot.pipelines.PodsearchbotPipeline']

LOG_LEVEL = 'INFO'

REFERER_ENABLED = False
ROBOTSTXT_OBEY = True

SPIDER_MODULES = ['PodSearchBot.spiders']
NEWSPIDER_MODULE = 'PodSearchBot.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

