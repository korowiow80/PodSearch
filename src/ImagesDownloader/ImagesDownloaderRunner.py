#! /bin/python

from ImagesDownloader import ImagesDownloader
from Resource.ResourceChecker import ResourceChecker

class FeedsDownloaderRunner:

    def __init__(self):
        self._iDler = ImagesDownloader()
        self._rc = ResourceChecker()

    def run(self):
        feedFilePaths = self._rc.getAllFeedPaths()
        for feedFilePath in feedFilePaths:
            self._iDler.handleFeed(feedFilePath)

        print('FeedsDownloaderRunner: INFO: Done.')

if __name__ == '__main__':
    fdr = FeedsDownloaderRunner()
    fdr.run()
