#! /bin/python

from ImagesDownloader import ImagesDownloader
from PathTool import PathTool

class FeedsDownloaderRunner:

    def __init__(self):
        self.iDler = ImagesDownloader()

    def run(self):
        feedFilePaths = PathTool.getAllFeedPaths()
        for feedFilePath in feedFilePaths:
            self.handleFeed(feedFilePath)

        print 'FeedsDownloaderRunner: INFO: Done.'

if __name__ == '__main__':
    fdr = FeedsDownloaderRunner()
    fdr.run()