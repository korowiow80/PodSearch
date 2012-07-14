import os
import ResourceChecker

class PathTool:
    """Represents a path of a file on the local filesystem.
    
    Has knowledge about our conventions regarding the filesystem layout."""

    def __init__(self):
        relativeProjectRoot = "../../../../"
        
        self._directoriesPath = relativeProjectRoot + "static/0-Directories/"
        self._feedListsPath = relativeProjectRoot + "static/1-Feedlists/"
        self._feedsPath = relativeProjectRoot + 'static/2-Feeds/'
        self._imagesPath = relativeProjectRoot + "web/img/"

    def getDirectoriesPath(self):
        return self._directoriesPath

    def getFeedsPath(self):
        return self._feedsPath
    
    def getFeedListsPath(self):
        return self._feedListsPath
    
    def getImagesPath(self):
        return self._imagesPath
