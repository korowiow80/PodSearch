"""TODO"""

import errno
import os

from Util.LoggerFactory.LoggerFactory import LoggerFactory


class ResourceHelper:
    
    _logger = LoggerFactory().getLogger('RessourceHelper')
    
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

