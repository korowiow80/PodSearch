import errno
import os

import UrlTool

class PathTool:
    
    _projectRoot = "../../../"
    
    def makeSurePathExists(self, path):
        """Makes sure a given path exists.
        Tries to create the given path, handles eventual failure.
        See: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python"""
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST: pass
            else: raise
        return

    def getDirectoryPath(self, domain):    
        """Derives the directory path from domain."""
        directoryPath = self._projectRoot + "static/0-Directories/" + domain + "/"
        return directoryPath

    def getFeedListFilePath(self, domain):
        """Derives the feedlist path from a given domain and fullDomain."""
        feedListFilePath = self._projectRoot + "static/1-Feedlists/" + domain + ".json"
        return feedListFilePath

    def getBasePath(self, ressourceTarget):
        basePath = os.path.dirname(ressourceTarget)
        return basePath

    def getImageFilePath(self, imageUrl):
        imagesPrefix = self.projectRoot + "web/img/"
        relativeRemoteLocation = self.getRelativePath(imageUrl)
        st = UrlTool()
        domain = st.getDomain(imageUrl)        
        imageFilePath = imagesPrefix + domain + relativeRemoteLocation
        return imageFilePath

    def getFeedFilePath(self, feedUrl):
        feedsPrefix = self.projectRoot + "static/2-Feeds/"
        relativeRemoteLocation = self.getRelativePath(feedUrl)
        st = UrlTool()
        domain = st.getDomain(feedUrl)
        feedFilePath = feedsPrefix + domain + relativeRemoteLocation        
        return feedFilePath

    def getRelativePath(self, url):
        if not url.startswith('http'): return url
        st = UrlTool()
        baseUrl = st.getBaseUrl(url)
        relativePath = url[len(baseUrl):]
        return relativePath

    def getRessourceTargetPath(self, ressourceType, ressourceUrl):
        if ressourceType == 'feed':
            ressourceTargetPath = self.getFeedFilePath(ressourceUrl)
        if ressourceType == 'image':
            ressourceTargetPath = self.getImageFilePath(ressourceUrl)        
        return ressourceTargetPath
