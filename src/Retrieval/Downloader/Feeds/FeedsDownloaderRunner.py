import os
import json

from FeedsDownloader import FeedsDownloader
from PathTool import PathTool


class FeedsDownloaderRunner:

    def __init__(self):
        self.fd = FeedsDownloader()
        self._pt = PathTool()

    def run(self):
        feedUrls = self.getAllFeedUrls()
        self.fd.downloadFeeds(feedUrls)
        print 'FeedsDownloaderRunner: INFO: Done.'
        
    def getAllFeedUrls (self):
        feedListsDirectory = self._pt.getFeedListsPath()
        relativeFeedListPaths = os.listdir(feedListsDirectory)
        allFeedUrls = []
        for relativeFeedListPath in relativeFeedListPaths:
            if relativeFeedListPath == 'feeds.list': continue
            if relativeFeedListPath == 'podster.list': continue
            if relativeFeedListPath == 'podcast.com.json': continue
            print relativeFeedListPath
            someFeedUrls = self.getFeedUrlsFromFeedList(relativeFeedListPath)
            for feedUrl in someFeedUrls:
                feedUrl = self._pt.stripWhiteSpace(feedUrl)
                allFeedUrls.append(feedUrl)
        return allFeedUrls
    
    def getFeedUrlsFromFeedList(self, feedListPath):
        feedListsDirectory = self._pt.getFeedListsPath()
        absoluteFeedListPath = feedListsDirectory + feedListPath
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