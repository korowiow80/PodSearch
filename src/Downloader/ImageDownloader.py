#! /bin/python

import os
import feedparser
import tldextract
import urlparse
import urllib
import os, errno

# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

class ImageDownloader:

    podcastDirectory = "../../static/2-Feeds"
    imageDirectory = "../../web/img/"

    def run(self):
        podcasts = self.getPodcasts()
        for podcast in podcasts:
            self.handlePodcast(podcast)

        print 'ImageDownloader: INFO: Done.'

    def handlePodcast (self, podcast):
        imgUrl = self.getImageUrl(podcast)
        # sanity check image url
        if not self.checkSanity(imgUrl): return

        # get image target location
        imageTarget = self.getImageTargetLocation(imgUrl)
        imageTarget = self.imageDirectory + imageTarget

        # make sure the analoguous location exists
        try:
            mkdir_p(os.path.dirname(imageTarget))
        except IOError:
            pass

        # download image to analogous location
        try:
            # urllib likes utf-8 better than unicode
            urllibImgUrl = imgUrl.encode('utf-8')

            urllib.urlretrieve(urllibImgUrl, filename=imageTarget)
            print "ImageDownloader.run: INFO: Downloaded %s to %s." % (imgUrl, imageTarget)
        except IOError:
            print "ImageDownloader.run: WARN: Failed to download %s to %s." % (imgUrl, imageTarget)
            return

    def getPodcasts (self):
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

    def checkSanity(self, imgUrl):
        if not imgUrl: return False

        if imgUrl.startswith('data:'): return False

        return True

    def getImageTargetLocation(self, imageUrl):
        # get image domain
        imgDomain = self.getImageDomain(imageUrl)
        # get relative path
        imgPath = urlparse.urlparse(imageUrl).path
        #imageUrl[imageUrl.index(imgDomain):]

        targetLocation = imgDomain + imgPath

        print "ImageDownloader.getImageTargetLocation: INFO: Parsed image target location '%s' from image URL '%s'" % (imgPath, imageUrl)
        return targetLocation

    def getImageDomain(self, podcast):
        domainTuple = tldextract.extract(podcast)

        # avoid introducing a leading with empty subdomains
        if domainTuple.subdomain == '':
            fullDomain = '.'.join(domainTuple[1:])
        else:
            fullDomain = '.'.join(domainTuple)

        return fullDomain

    def parsePodcast (self, podcast):
        try:
            podcast = feedparser.parse(podcast)
        except UnicodeDecodeError:
            print "ImageDownloader.parseDownload: WARN: Podcast '%s' contains undecodable characters." % podcast
            return

        return podcast

if __name__ == '__main__':
    id = ImageDownloader()
    id.run()