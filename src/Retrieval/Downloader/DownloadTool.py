import os
import urllib
import urlparse
import httplib
import tldextract

from Scrapy.spiders.SpiderTool import SpiderTool


class DownloadTool:

    projectRoot = "../../../"

    def download (self, ressourceType, ressourceUrl):
        if not self.sanityCheckUrl(ressourceUrl): return
        if ressourceUrl.endswith('/'): ressourceUrl = ressourceUrl[:-1] 
        ressourceTarget = self.getRessourceTarget(ressourceType, ressourceUrl)
        basePath = self.getBasePath(ressourceTarget)
        st = SpiderTool()
        st.makeSurePathExists(basePath)
        self._download(ressourceType, ressourceUrl, ressourceTarget)
    
    def _download (self, ressourceType, ressourceUrl, ressourceTarget):
        print "Downloading %s from %s to %s" % (ressourceType, ressourceUrl, ressourceTarget)
        # TODO multiprocess the acutal downloading
        # TODO make sure we don't already downloaded this very image


        # urllib likes utf-8 better than unicode
        ressourceUrl = ressourceUrl.encode('utf-8')

        # Disable HTTP Basic Authentification
        urllib.FancyURLopener.prompt_user_passwd = lambda *a, **k: (None, None)
        
        try:
            urllib.urlretrieve(ressourceUrl, ressourceTarget)
        except IOError, httplib.InvalidURL:
            pass

    def sanityCheckUrl (self, url):
        if not url: return False
        if url.endswith('://'): return False
        # skip dataUrls
        if url.startswith('data:'): return False

        # TODO do real url validation here ... like Django does
        return True

    def getRessourceTarget(self, ressourceType, ressourceUrl):
        if ressourceType == 'feed':
            ressourceTarget = self.getFeedFilePath(ressourceUrl)
        if ressourceType == 'image':
            ressourceTarget = self.getImageFilePath(ressourceUrl)        
        return ressourceTarget

    def getBasePath(self, ressourceTarget):
        basePath = os.path.dirname(ressourceTarget)
        return basePath

    def getImageFilePath(self, imageUrl):
        imagesPrefix = self.projectRoot + "web/img/"
        relativeRemoteLocation = self.getRelativePath(imageUrl)
        st = SpiderTool()
        domain = st.getDomain(imageUrl)        
        imageFilePath = imagesPrefix + domain + relativeRemoteLocation
        return imageFilePath

    def getFeedFilePath(self, feedUrl):
        feedsPrefix = self.projectRoot + "static/2-Feeds/"
        relativeRemoteLocation = self.getRelativePath(feedUrl)
        st = SpiderTool()
        domain = st.getDomain(feedUrl)
        feedFilePath = feedsPrefix + domain + relativeRemoteLocation        
        return feedFilePath

    def getRelativePath(self, url):
        if not url.startswith('http'): return url
        st = SpiderTool()
        baseUrl = st.getBaseUrl(url)
        relativePath = url[len(baseUrl):]
        return relativePath
