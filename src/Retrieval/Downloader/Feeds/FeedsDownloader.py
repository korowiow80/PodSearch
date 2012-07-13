#! /bin/python

from DownloaderTool.DownloaderTool import DownloaderTool


class FeedsDownloader:
    
    def __init__ (self):
        self.dt = DownloaderTool()
    
    def downloadFeeds(self, feedUrls):
        for feedUrl in feedUrls:
            self.handleFeed(feedUrl)
    
    def handleFeed(self, feedUrl):
        self.dt.download('feed', feedUrl)