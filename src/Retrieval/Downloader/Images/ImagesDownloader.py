#! /bin/python

import feedparser

from ResourceDownloader import ResourceDownloader


class ImagesDownloader:
    _projectRoot = '../../../'

    def __init__ (self):
        self.dt = ResourceDownloader()

    def handleFeed (self, relativeFeedFilePath):
        """Downloads a single image gathered from a given feed."""
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
