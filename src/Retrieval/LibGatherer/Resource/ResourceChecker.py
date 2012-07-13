import errno
import os
import mimetypes
import posixpath

import magic

import Url.UrlTool

class ResourceChecker:
    
    # really valid is only 'application/rss+xml'.
    # see http://stackoverflow.com/questions/595616/what-is-the-correct-mime-type-to-use-for-an-rss-feed
    validFeedMimeTypes = ['application/rss+xml',
                          'application/xml',
                          'text/xml']
    
    def __init__(self):
        pass

    def checkRemoteResource(self, ressourceType, url):
        """Checks the URL for sanity according to the ressourceType.
        Returns True if the URL is sane for this ressourceType, otherwise
        False."""
        if not url:
            return False
        if not ressourceType:
            return False #TODO we should raise here

        if not self._sanityCheckGeneralUrl(url):
            return False
        
        if ressourceType == 'feed':
            sanity = self._checkFeedUrl(url)
        if ressourceType == 'image':
            sanity = self._checkImageUrl(url)

        return sanity
    
    def _sanityCheckGeneralUrl(self, url):
        """Checks an URL for sanity. Returns True if the URL is sane, otherwise
        False."""

        if url.endswith('://'): return False

        # TODO do real url validation here ... like Django does
        
        return True
        
    def _checkImageUrl(self, url):
        """Checks an image URL for sanity. Returns True if the URL is sane,
        otherwise False."""
        
        # We skip dataUrls
        if url.startswith('data:'):
            return False
        
        sanity = self.checkImageMimeType(url)

        return sanity
    
    def _checkFeedUrl(self, url):
        """Checks an URL of a feed for sanity. Returns True if the URL is sane,
        otherwise False."""

        if self._checkFeedUrlFileType(url):
            return True

        feedFilename = self.getFilename(url)
        if not self._pt.checkFeedMimeType(feedFilename):
            return False
        
        sanity = self.checkFeedFileType(url)
        if not sanity:
            print "UrlTool: WARN: Did not recognize mime media type of feed %s." % (url)
        return sanity
    
    def _checkFeedUrlFileType(self, url):
        # Google's Feedburner always does the right thing.^tm
        if url.startswith('http://feeds.feedburner.com/'):
            return True
        
        # If the URL seems sane, we believe that, too.
        if url.endswith('/rss'):
            return True
        
        return False
    
    def checkLocalResource(self, path, type):
        if type == "directory":
            raise # not yet implemented
        if type == "feed":
            return self._checkLocalFeed(path)
        if type == "image":
            return self.checkImage(path)
    
    def _checkLocalFeed(self, feedPath):
        """Checks a path of a feed for sanity."""
        if os.path.isdir(feedPath):
            return False
        if self._checkLocalFeedHtml(feedPath):
            return False
        if self._checkLocalFeedMimeType(feedPath):
            return True
        if self._checkLocalFeedMagic(feedPath):
            return True
        return False

    def _checkLocalFeedMagic(self, feedPath):
        """Checks the mimetype of a given local file."""
        mime = magic.open(magic.MAGIC_MIME)
        mime.load()
        mimetype = mime.file(feedPath)

        mimetype = mimetype.split('; ')[0]
        if mimetype in PathTool.validFeedMimeTypes:
            return True
        return False
    
    def _checkLocalFeedMimeType(self, filename):
        """Checks mimetype by filename."""
        mimetype, encoding = mimetypes.guess_type(filename, strict=False)
        if mimetype in self.validFeedMimeTypes:
            return True
        return False
    
    def _checkLocalFeedHtml(self, feedPath):
        """Checks for a feed given by path to be a html file."""
        
        with open(feedPath, 'r') as feed:
            feed = feed.read()
            feed = ' '.join(feed.split())
        if feed.startswith("<html>") or feed.endswith("</html>"):
            return True
        return False
