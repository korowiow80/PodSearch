#! /bin/python

import os
import json

from DownloadTool import DownloadTool

class FeedDownloader:
    
    projectRoot = "../../../"

    def __init__ (self):
        self.dt = DownloadTool()

    def run (self):
        feedUrls = self.getAllFeedUrls()
        self.downloadFeeds(feedUrls)
        print 'FeedDownloader: INFO: Done.'

    def getAllFeedUrls (self):
        feedListDirectory = self.projectRoot + "static/1-Feedlists/"
        relativeFeedListPaths = os.listdir(feedListDirectory)
        allFeedUrls = []
        for relativeFeedListPath in relativeFeedListPaths:
            print relativeFeedListPath
            if relativeFeedListPath == 'feeds.list': continue
            if relativeFeedListPath == 'podster.list': continue
            someFeedUrls = self.getFeedUrlsFromFeedList(relativeFeedListPath)
            for feedUrl in someFeedUrls:
                allFeedUrls.append(feedUrl)
        return allFeedUrls
    
    def getFeedUrlsFromFeedList(self, feedListPath):
        feedListDirectory = self.projectRoot + "static/1-Feedlists/"
        absoluteFeedListPath = feedListDirectory + feedListPath
        feedUrls = []
        with open(absoluteFeedListPath, 'r') as f:
            contents = f.read()
            feedItems = json.loads(contents)
            for feedItem in feedItems:
                feedUrls.append(feedItem['link'])
                #TODO get the title, too
        return feedUrls
    
    def downloadFeeds(self, feedUrls):
        for feedUrl in feedUrls:
            self.downloadFeed(feedUrl)
    
    def downloadFeed(self, feedUrl):
        self.dt.download('feed', feedUrl)
            
if __name__ == '__main__':
    fd = FeedDownloader()
    fd.run()