import os
import posixpath
import tldextract
import urllib
import urlparse

from Util.PathTool.PathTool import PathTool
from os import path


class Resource:
    """Represents both an URL of a resource on a remote file system and a
    corresponding path to the local representation."""

    _pt = PathTool()

    def __init__(self, url, resource_type):
        self._url = ''
        self.setUrl(url)
        self._type = ''
        self._id = ''
        self._path = ''
        self.setType(resource_type)
    
    def setUrl(self, url):
        self._url = url
    
    def setType(self, resource_type):
        self._type = resource_type
        self._setPath()
        self._setId()
        self._setId()
        
    def _setPath(self):
        """Derives the download destination."""
        if self._type == "directory":
            self._setFeedListPath()
        if self._type == "feed":
            self._setFeedPath()
        if self._type == "image":
            self._setImagePath()

    def _setId(self):
        """The id of a resource is its id relative to the corresponding
        resource directory."""
        id = self.getPath()

        id = id.lstrip('/.')
        while id.startswith('static/2-Feeds/'):
            id = id[len('static/2-Feeds/'):]
            id = id.lstrip('/.')
        
        id = id.rstrip('./')    # just to be sure
        
        self._id = id
    
    def _setDirectoryPath(self):
        """Derives the directory path from domain."""
        domain = self.getDomain()
        directoriesPath = self._pt.getDirectoriesPath()
        directoryPath = directoriesPath + domain + "/"
        self._path = directoryPath

    def _setFeedListPath(self):
        """Derives the path of a feedlist from a given url."""
        domain = self.getDomain()
        feedListsPath = self._pt.getFeedListsPath()
        #feedListsPath = feedListsPath[3:] # somehow we need to go up one level for the crawlers
        feedListPath = feedListsPath + domain + ".txt"
        self._path = feedListPath

    def _setFeedPath(self):
        """Derives the path of a feed from a given url."""
        feedsPath = self._pt.getFeedsPath()
        relativeRemoteLocation = self.getRelativeUrl()
        domain = self.getDomain()
        prefixFolder = domain[:2] + "/"
        feedFilePath = feedsPath + prefixFolder + domain + relativeRemoteLocation        
        self._path = feedFilePath
    
    def _setImagePath(self):
        """Derives the path of an image from a given url."""
        imagesPrefix = self._pt.getImagesPath()
        relativeRemoteLocation = self.getPath()
        domain = self.getDomain()
        imageFilePath = imagesPrefix + domain + relativeRemoteLocation
        self._path = imageFilePath

    def getAbsoluteUrl(self):
        """Returns the absolute URL for an relative URL and a baseurl."""  
        if self._url.startswith('http'):
            return self._url
        else:
            absoluteUrl = self.getBaseUrl() + self.getRelativeUrl()
            return absoluteUrl

    def getBaseUrl(self):
        """Derives the baseUrl from a given url."""
        o = urlparse.urlparse(self._url)
        baseUrl = o.scheme + '://' + o.netloc
        return baseUrl

    def getDomain(self):
        """Extracts the full and the top-level domain from a given URL.
        By our convention, we skip the sub-domain, if it is 'www'."""
        extract = tldextract.extract(self._url)
        if extract.subdomain and extract.subdomain != 'www' and \
                extract.subdomain != 'api':
            domain = ".".join(extract)
        else:
            domain = ".".join(extract[1:])
        return domain
    
    def getRelativeUrl(self):
        """Derives the filename from a given url."""
        if not self._url.startswith('http'):
            return self._url
        baseUrl = self.getBaseUrl()
        url = self.getAbsoluteUrl()
        relativeUrl = url[len(baseUrl):]
        return relativeUrl
    
    def getFilename(self):
        """Derives the filename from a given URL."""
        urlParts = urllib.parse.urlsplit(self._url)
        remotePath = urlParts.path
        filename = posixpath.basename(remotePath)
        return filename
    
    def getBasePath(self):
        """TODO understand and document me!"""
        basePath = os.path.dirname(self.getPath())
        
        # reconstruct path if it does not end with an filename extension
        basePathEnd = basePath.split('/')[-1]
        ressourceTargetEnd = self.getPath().split('/')[-1]
        if basePathEnd == ressourceTargetEnd and \
           basePath[-1] != '/':
            basePath = os.sep.join(basePath.split('/')[:-1])
        
        return basePath
        
    def getSpiderName(self):
        """Derives the spider name from the given domain and fullDomain.
        By general convention the first letter of a class gets capitalized."""
        domain = self.getDomain()
        try:
            spiderName = domain[0].upper() + domain.replace('.', '_')[1:]
        finally:
            return spiderName
  
    def getPath(self):
        return self._path

    def getId(self):
        return self._id
