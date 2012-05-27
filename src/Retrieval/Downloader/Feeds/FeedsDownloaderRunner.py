import os
import json

from FeedsDownloader import FeedsDownloader
from PathTool import PathTool


class FeedsDownloaderRunner:

    def __init__(self):
        self.fd = FeedsDownloader()

    def run(self):
        feedUrls = self.getAllFeedUrls()
        self.fd.downloadFeeds(feedUrls)
        print 'FeedsDownloaderRunner: INFO: Done.'
        
    def getAllFeedUrls (self):
        feedListDirectory = PathTool.getFeedListsPath()
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
        feedListDirectory = self._projectRoot + "static/1-Feedlists/"
        absoluteFeedListPath = feedListDirectory + feedListPath
        feedUrls = []
        with open(absoluteFeedListPath, 'r') as f:
            contents = f.read()
            feedItems = json.loads(contents)
            for feedItem in feedItems:
                feedUrls.append(feedItem['link'])
                #TODO get the title, too
        return feedUrls

if __name__ == '__main__':
    fdr = FeedsDownloaderRunner()
    fdr.run()