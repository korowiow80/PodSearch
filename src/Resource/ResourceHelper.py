""""""

import errno
import os

from Util.LoggerFactory.LoggerFactory import LoggerFactory
from Util.PathTool import PathTool
from ResourceChecker import ResourceChecker

class ResourceHelper:
    
    _logger = LoggerFactory().getLogger('RessourceHelper')
    _pt = PathTool.PathTool()
    _rc = ResourceChecker()
    
    def __init__(self):
        pass
    
    def ensurePathExists(self, path):
        """Makes sure a given path exists.
        Tries to create the given path, handles eventual failure.
        See: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python"""
        
        ResourceHelper._logger.info('Ensuring path %s exists.' % path)
        
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST: return
            if exc.errno == errno.ENOTDIR: return
            raise
        return

    def stripWhitespace(self, filename):
        """Substitutes all space literals (' ', '\n', '\t' etc.) with nothing."""
        filename = ' '.join(filename.split())
        return filename
    
    def getAllFeedPaths(self):
        """Gathers all feed paths"""
        feedsPath = self._pt.getFeedsPath()
        relativeFeedFilePaths = []
        for root, dirs, files in os.walk(feedsPath):
            for filePath in files:
                relativePath = os.path.join(root, filePath)
                if self._rc.check_local_resource(relativePath, 'feed'):
                    relativeFeedFilePaths.append(relativePath)
            if '/me/' in root:
                break
        return relativeFeedFilePaths

