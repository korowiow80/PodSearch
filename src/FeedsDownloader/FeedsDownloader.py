#! /bin/python

from Downloader.ResourceDownloader import ResourceDownloader


class FeedsDownloader:
    
    def __init__ (self):
        self.dt = ResourceDownloader()
    
    def downloadFeeds(self, feedUrls):
        for feedUrl in feedUrls:
            self.handleFeed(feedUrl)
    
    def handleFeed(self, feedUrl):
        self.dt.download('feed', feedUrl)
