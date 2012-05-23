#! /bin/python

import os
import feedparser

from DownloadTool import DownloadTool


class ImageDownloader:

    def run(self):
        podcasts = self.getAllFeedUrls()
        for podcast in podcasts:
            self.handlePodcast(podcast)

        print 'ImageDownloader: INFO: Done.'

    def handlePodcast (self, podcast):
        imgUrl = self.getImageUrl(podcast)
        # sanity check image url
        if not self.checkSanity(imgUrl): return
        
        self.downloadImage(imgUrl)

    def downloadImage (self, imgUrl):
        # downloads image to analogous location
        dt = DownloadTool()
        dt.download("image", imgUrl)
        
    def getAllFeedUrls (self):
        podcasts = os.listdir(self.podcastDirectory)
        return podcasts

    def getImageUrl(self, podcast):
        podcast = self.podcastDirectory + os.sep + podcast

        p = self.parsePodcast(podcast)
        if not p: return

        try:
            imageUrl = p.feed.image.href
        except AttributeError:
            print "ImageDownloader.getImageUrl: WARNING: Podcast %s did not contain an image." % podcast
            return

        print "ImageDownloader.getImageUrl: INFO: Parsed image URL '%s' from podcast '%s'" % (imageUrl, podcast)
        return imageUrl

    def parsePodcast (self, podcast):
        try:
            podcast = feedparser.parse(podcast)
        except UnicodeDecodeError:
            print "ImageDownloader.parseDownload: WARN: Podcast '%s' contains undecodable characters." % podcast
            return

        return podcast

if __name__ == '__main__':
    ImageDownloader().run()