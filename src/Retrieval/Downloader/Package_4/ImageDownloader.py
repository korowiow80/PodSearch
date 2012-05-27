#! /bin/python

import os
import feedparser

from DownloaderTool import DownloaderTool


class ImageDownloader:
    projectRoot = '../../../'

    def __init__ (self):
        self.dt = DownloaderTool()

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
            return podcast
        except (UnicodeDecodeError, IndexError):
            print "ImageDownloader.parseDownload: WARN: Podcast '%s' contains undecodable characters." % podcast

    def downloadImage (self, imgUrl):
        self.dt.download("image", imgUrl)
