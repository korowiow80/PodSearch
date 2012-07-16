from Util.LoggerFactory.LoggerFactory import LoggerFactory


class PathTool:
    """Has knowledge about our conventions regarding the file system layout."""

    _logger = LoggerFactory().getLogger('PathTool')

    def __init__(self):
        PathTool._logger.debug('Initializing.')
        relativeProjectRoot = "../../"
        self._directoriesPath = relativeProjectRoot + "static/0-Directories/"
        self._feedListsPath = relativeProjectRoot + "static/1-Feedlists/"
        self._feedsPath = relativeProjectRoot + 'static/2-Feeds/'
        self._imagesPath = relativeProjectRoot + "web/img/"
        PathTool._logger.debug('Initialized.')

    def getDirectoriesPath(self):
        return self._directoriesPath

    def getFeedsPath(self):
        return self._feedsPath
    
    def getFeedListsPath(self):
        return self._feedListsPath
    
    def getImagesPath(self):
        return self._imagesPath
