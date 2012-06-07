import errno
import os
import re
import UrlTool


class PathTool:
    
    def __init__(self):
        theirProjectRoot = "../../../../"
        
        self._directoriesPath = theirProjectRoot + "static/0-Directories/"
        self._feedListsPath = theirProjectRoot + "static/1-Feedlists/"
        self._feedsPath = theirProjectRoot + 'static/2-Feeds/'
        self._imagesPath = theirProjectRoot + "web/img/"
    
        self._ut = UrlTool.UrlTool()

    def ensurePathExists(self, path):
        """Makes sure a given path exists.
        Tries to create the given path, handles eventual failure.
        See: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python"""
        
        print "PathTool: Ensuring path %s exists." % path #TODO
        
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST: return
            if exc.errno == errno.ENOTDIR: return
            raise
        return

    def stripWhiteSpace(self, filename):
        # substitute all space literals (' ', '\n', '\t' etc.) with nothing
        filename = re.sub(r'\s', '', filename)
        return filename

    def getBasePath(self, ressourceTarget):
        basePath = os.path.dirname(ressourceTarget)
        
        # reconstruct path if it does not end with an filename extension
        basePathEnd = basePath.split('/')[-1]
        ressourceTargetEnd = ressourceTarget.split('/')[-1]
        if basePathEnd == ressourceTargetEnd and \
           basePath[-1] != '/':
            basePath = os.sep.join(basePath.split('/')[:-1])
        
        return basePath

    def getDirectoriesPath(self):
        return self._directoriesPath

    def getDirectoryPath(self, domain):
        """Derives the directory path from domain."""
        directoriesPath = self.getDirectoriesPath()
        directoryPath = directoriesPath + domain + "/"
        return directoryPath
    
    def getFeedsPath(self):
        return self._feedsPath
    
    def getFeedListsPath(self):
        return self._feedListsPath

    def getFeedListPath(self, url):
        """Derives the path of a feedlist from a given domain."""
        domain = self._ut.getDomain(url)
        feedListsPath = self.getFeedListsPath()
        feedListsPath = feedListsPath[3:] # somehow we need to go up one level for the crawlers
        feedListPath =  feedListsPath + domain + ".json"
        return feedListPath

    def getFeedPath(self, feedUrl):
        """Derives the path of a feed from a given domain."""
        feedsPath = self.getFeedsPath()
        relativeRemoteLocation = self._ut.getRelativeUrl(feedUrl)
        domain = self._ut.getDomain(feedUrl)
        prefixFolder = domain[:2] + "/"
        feedFilePath = feedsPath + prefixFolder + domain + relativeRemoteLocation        
        return feedFilePath

    def getFeedPaths(self):
        """Gathers alls feed paths"""
        feedsPath = self.getFeedsPath()
        relativeFeedFilePaths = []
        for root, dirs, files in os.walk(feedsPath):
            for filePath in files:
                relativePath = os.path.join(root, filePath)
                relativeFeedFilePaths.append(relativePath)
        return relativeFeedFilePaths

    def getImagesPath(self):
        return self._imagesPath

    def getImagePath(self, imageUrl):
        imagesPrefix = self.getImagesPath()
        relativeRemoteLocation = self.getRelativePath(imageUrl)
        domain = self._ut.getDomain(imageUrl)        
        imageFilePath = imagesPrefix + domain + relativeRemoteLocation
        return imageFilePath

    def getRessourceTargetPath(self, ressourceType, ressourceUrl):
        if ressourceType == 'feed':
            ressourceTargetPath = self.getFeedPath(ressourceUrl)
        if ressourceType == 'image':
            ressourceTargetPath = self.getImagePath(ressourceUrl)        
        return ressourceTargetPath
