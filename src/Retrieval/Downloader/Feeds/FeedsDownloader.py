#! /bin/python

from DownloaderTool import DownloaderTool


class FeedsDownloader:
    
    def __init__ (self):
        self.dt = DownloaderTool()
    
    def downloadFeeds(self, feedUrls):
        for feedUrl in feedUrls:
            self.downloadFeed(feedUrl)
    
    def downloadFeed(self, feedUrl):
        self.dt.download('feed', feedUrl)