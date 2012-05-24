#! /bin/python

import os
import feedparser

from DownloadTool import DownloadTool


class ImageDownloader:
    projectRoot = '../../../'

    def __init__ (self):
        self.dt = DownloadTool()

    def run(self):
        relativeFeedFilePaths = self.getAllFeedFilePaths()
        for relativeFeedFilePath in relativeFeedFilePaths:
            self.handleFeed(relativeFeedFilePath)

        print 'ImageDownloader: INFO: Done.'

    def getAllFeedFilePaths (self):
        feedDirectoryPath = self.projectRoot + 'static/2-Feeds'
        relativeFeedFilePaths = []
        for root, dirs, files in os.walk(feedDirectoryPath, topdown=False):
            for filePath in files:
                relativePath = os.path.join(root, filePath)
                relativeFeedFilePaths.append(relativePath)
        return relativeFeedFilePaths

    def handleFeed (self, relativeFeedFilePath):
        imgUrl = self.getImageUrl(relativeFeedFilePath)
        self.downloadImage(imgUrl)

    def getImageUrl(self, podcastFeedFilePath):
        p = self.parsePodcast(podcastFeedFilePath)
        if not p: return

        try:
            imageUrl = p.feed.image.href
        except AttributeError:
            print "ImageDownloader.getImageUrl: WARNING: Podcast %s did not contain an image." % podcastFeedFilePath
            return

        print "ImageDownloader.getImageUrl: INFO: Parsed image URL '%s' from podcastFeedFilePath '%s'" % (imageUrl, podcastFeedFilePath)
        return imageUrl

    def parsePodcast(self, podcast):
        try:
            podcast = feedparser.parse(podcast)
        except UnicodeDecodeError:
            print "ImageDownloader.parseDownload: WARN: Podcast '%s' contains undecodable characters." % podcast
            return

        return podcast

    def downloadImage (self, imgUrl):
        self.dt.download("image", imgUrl)

if __name__ == '__main__':
    ImageDownloader().run()