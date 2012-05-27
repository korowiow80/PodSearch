import errno
import os

import UrlTool


class PathTool:
    
    _projectRoot = "../../../"
    
    _directoriesPath = _projectRoot + "static/0-Directories/"
    _feedListsPath = _projectRoot + "static/1-Feedlists/"
    _feedsPath = _projectRoot + 'static/2-Feeds'
    _imagesPath = _projectRoot + "web/img/"

    _ut = UrlTool()

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

    def getBasePath(self, ressourceTarget):
        basePath = os.path.dirname(ressourceTarget)
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

    def getFeedListPath(self, domain):
        """Derives the path of a feedlist from a given domain."""
        feedListPath = self.getFeedListsPath() + domain + ".json"
        return feedListPath

    def getFeedPath(self, feedUrl):
        """Derives the path of a feed from a given domain."""
        feedsPath = self.getFeedsPath()
        relativeRemoteLocation = self.getRelativePath(feedUrl)
        domain = self._ut.getDomain(feedUrl)
        feedFilePath = feedsPath + domain + relativeRemoteLocation        
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
