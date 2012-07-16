#! /bin/python

import feedparser

from Downloader.ResourceDownloader import ResourceDownloader
from Util.LoggerFactory.LoggerFactory import LoggerFactory


class ImagesDownloader:
    _projectRoot = '../../../'

    _logger = LoggerFactory().getLogger('ImagesDownloader')
    _rd = ResourceDownloader()
    
    def __init__ (self):
        pass

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
            warnString = 'Feed %s did not contain an image.' \
                         % podcastFeedFilePath
            ImagesDownloader._logger.warn(warnString)
            return

        msg = "Parsed image URL '%s' from feed '%s'" % (imageUrl, podcastFeedFilePath)
        ImagesDownloader._logger.info(msg)
        return imageUrl

    def parsePodcast(self, podcast):
        try:
            podcast = feedparser.parse(podcast)
            return podcast
        except (UnicodeDecodeError, IndexError):
            msg = "Feed '%s' contains undecodable characters." % podcast
            ImagesDownloader._logger.warn(msg)

    def downloadImage (self, imgUrl):
        ImagesDownloader._rd.download("image", imgUrl)
