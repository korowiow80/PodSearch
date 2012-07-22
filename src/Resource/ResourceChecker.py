import os
import mimetypes

import magic

from Resource.Resource import Resource
from Util.PathTool import PathTool
from Util.LoggerFactory.LoggerFactory import LoggerFactory

class ResourceChecker:
    
    _logger = LoggerFactory().getLogger('ResourceChecker')
    
    # really valid is only 'application/rss+xml'.
    # see http://stackoverflow.com/questions/595616/what-is-the-correct-mime-type-to-use-for-an-rss-feed
    # not quite right, anything non-toxic
    acceptedFeedMimeTypes = ['text/html', # test for HTML later
                            'text/plain',
                            'text/x-php', # test for php later
                            'text/x-c++'] # test for c++ later
    # not quite wrong
    validFeedMimeTypes = ['application/rss+xml',
                          'application/xml',
                          'text/xml'] + acceptedFeedMimeTypes
    
    def __init__(self):
        self._pt = PathTool.PathTool()

    def checkRemoteResource(self, resourceType, url):
        """Checks the URL for sanity according to the resourceType.
        Returns True if the URL is sane for this resourceType, otherwise
        False."""
        if not url:
            return False
        if not resourceType:
            return False #TODO we should raise here

        if not self._sanityCheckGeneralUrl(url):
            return False
        
        if resourceType == 'feed':
            sanity = self._checkFeedUrl(url)
        if resourceType == 'image':
            sanity = self._checkImageUrl(url)

        return sanity
    
    def _sanityCheckGeneralUrl(self, url):
        """Checks an URL for sanity. Returns True if the URL is sane, otherwise
        False."""

        if url.endswith('://'):
            return False

        # TODO do real url validation here ... like Django does
        
        return True
        
    def _checkImageUrl(self, url):
        """Checks an image URL for sanity. Returns True if the URL is sane,
        otherwise False."""
        
        # We skip dataUrls
        if url.startswith('data:'):
            return False
        
        sanity = self._checkRemoteImageMimeType(url)

        return sanity
    
    def _checkFeedUrl(self, url):
        """Checks an URL of a feed for sanity. Returns True if the URL is sane,
        otherwise False."""

        if self._checkFeedUrlFileType(url):
            return True

        resource_type = 'feed'

        feedFilename = Resource(url, resource_type).getFilename()
        if not self._checkRemoteFeedMimeType(feedFilename):
            return False
        
        sanity = self._checkRemoteFeedMimeType(url)
        if not sanity:
            msg = "Did not recognize mime media type of feed %s." % (url)
            ResourceChecker._logger.warn(msg)
        return sanity
    
    def _checkFeedUrlFileType(self, url):
        # Google's Feedburner always does the right thing.^tm
        if url.startswith('http://feeds.feedburner.com/'):
            return True
        
        # If the URL seems sane, we believe that, too.
        if url.endswith('/rss'):
            return True
        
        return False
    
    def checkLocalResource(self, path, resourceType):
        if resourceType == "directory":
            raise # not yet implemented
        if resourceType == "feed":
            return self._checkLocalFeed(path)
        if resourceType == "image":
            raise # not yet implemented 
            #return self._checkLocalImage(path)
    
    def _checkLocalFeed(self, feedPath):
        """Checks a path of a feed for sanity."""
        
        # from cheapest to most expensive
        if os.path.isdir(feedPath):
            return False
        if self._checkLocalFeedMimeType(feedPath):
            return True
        if self._checkLocalFeedMagic(feedPath):
            return True
        #if self._checkLocalFeedBadHeadAndTail(feedPath):
            #return False
        #TODO check for binary
        return False
    
    def _checkRemoteFeedMimeType(self, filename):
        return self._checkLocalFeedMimeType(filename)
    
    def _checkLocalFeedMimeType(self, filename):
        """Checks mimetype of a given file by looking at its filename."""
        mimetype, encoding = mimetypes.guess_type(filename, strict=False)
        if mimetype in self.validFeedMimeTypes:
            return True
        return False

    def _checkLocalFeedMagic(self, feedPath):
        """Checks the mimetype of a given local file by looking at the file header."""
        mimetype = magic.from_file(feedPath.encode('utf-8'), mime=True)
        mimetype = mimetype.decode()
        mimetype = str(mimetype).split('; ')
        mimetype = mimetype[0]
        if mimetype in self.validFeedMimeTypes:
            return True
        msg = "Skipping %s %s." % (mimetype, feedPath)
        ResourceChecker._logger.warn(msg)
        return False
    
    def _checkRemoteImageMimeType(self, filename):
        return self._checkLocalImageMimeType(filename)
    
    def _checkLocalImageMimeType(self, filename):
        """Checks mimetype by filename."""
        mimetype, encoding = mimetypes.guess_type(filename, strict=False)
        if "image/" in mimetype:
            return True
        return False
    
    def _checkLocalFeedBadHeadAndTail(self, feedPath):
        """Checks for a feed given by path to be a html file."""
        
        bad_heads = ['<html>', '<?php', '#include']
        bad_tails = ['</html>', '?>', '}']
        
        with open(feedPath, 'rb') as feed:
            feed = feed.read()
            try:
                feed = feed.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    feed = feed.decode('latin-1')
                except UnicodeDecodeError:
                    raise
            feed = ' '.join(feed.split())

        for head in bad_heads:
            if feed.startswith(head):
                return True
        for tail in bad_tails:
            if feed.startswith(tail):
                return True
        return False
