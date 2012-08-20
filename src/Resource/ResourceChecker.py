"""Central sanity checking facility for PodSearch."""

import httplib
import os
import mimetypes
import socket
import urlparse

import magic

from Resource import Resource
from UrlValidator import UrlValidator
from Util.PathTool import PathTool
from Util.LoggerFactory.LoggerFactory import LoggerFactory

class ResourceChecker:
    """Checks resources for sanity on various levels."""
    
    _logger = LoggerFactory().getLogger('ResourceChecker')
    
    # really valid is only 'application/rss+xml'.
    # see http://stackoverflow.com/questions/595616/
    # not quite right but also not toxic
    not_quite_right_feed_mime_types = ['text/html', # test for HTML later
                                       'text/plain',
                                       'text/x-php', # test for php later
                                       'text/x-c++'] # test for c++ later
    not_quite_wrong_feed_mime_types = ['application/rss+xml',
                                       'application/xml',
                                       'text/xml']
    valid_feed_mime_types = not_quite_wrong_feed_mime_types
    
    def __init__(self):
        self._pt = PathTool.PathTool()

    def check_remote_resource(self, resource_type, url):
        """Checks the URL for sanity according to the resource_type.
        Returns True if the URL is sane for this resource_type, otherwise
        False."""
        
        if not url:
            return False
        if not resource_type:
            return False # TODO we should raise here

        if not self._check_general_url(url):
            return False
        
        if resource_type == 'feed':
            sanity = self._check_feed_url(url)
        elif resource_type == 'image':
            sanity = self._check_image_url(url)
            
        if sanity:
            sanity = self._check_remote_existence(url)

        return sanity
    
    def _check_general_url(self, url):
        """Checks an URL for sanity. Returns True if the URL is sane, otherwise
        False.
        >>> from ResourceChecker import ResourceChecker
        >>> resource_checker = ResourceChecker()
        >>> resource_checker._check_general_url("http://example.com")
        True"""

        url_validator = UrlValidator()
        sanity = url_validator.validate(url)
        
        return sanity

    def _check_image_url(self, url):
        """Checks an image URL for sanity. Returns True if the URL is sane,
        otherwise False."""
        
        # We skip dataUrls
        if url.startswith('data:'):
            return False
        
        sanity = self._check_remote_image_mime_type(url)

        return sanity
    
    def _check_feed_url(self, url):
        """Checks an URL of a feed for sanity. Returns True if the URL is sane,
        otherwise False."""

        if self._check_feed_url_file_type(url):
            return True

        resource_type = 'feed'

        feed_filename = Resource(url, resource_type).get_filename()
        if not self._check_remote_feed_mime_type(feed_filename):
            return False
        
        sanity = self._check_remote_feed_mime_type(url)
        if not sanity:
            msg = "Did not recognize mime media type of feed %s." % (url)
            ResourceChecker._logger.warn(msg)
        return sanity
    
    def _check_feed_url_file_type(self, url):
        """"""
        # Google's Feedburner always does the right thing.^tm
        if url.startswith('http://feeds.feedburner.com/'):
            return True
        
        # If the URL seems sane, we believe that, too.
        if url.endswith('/rss'):
            return True
        
        return False
    
    def check_local_resource(self, path, resourceType):
        """Checks a local resource of any kind for sanity.
        
        TODO doctest
        """
        if resourceType == "directory":
            raise # not yet implemented
        if resourceType == "feed":
            return self._check_local_feed(path)
        if resourceType == "image":
            raise # not yet implemented 
            #return self._checkLocalImage(path)
    
    def _check_local_feed(self, feed_path):
        """Checks a path of a local feed for sanity."""
        
        # from cheapest to most expensive
        if os.path.isdir(feed_path):
            return False
        if self._check_local_feed_mime_type(feed_path):
            return True
        if self._check_local_feed_magic(feed_path):
            return True
        #if self._check_local_feed_bad_ends(feed_path):
            #return False
        #TODO check for binary
        return False
    
    def _check_remote_feed_mime_type(self, filename):
        """"""
        return self._check_local_feed_mime_type(filename)
    
    def _check_local_feed_mime_type(self, filename):
        """Checks mimetype of a given file by looking at its filename."""
        mimetype, encoding = mimetypes.guess_type(filename, strict=False)
        if mimetype in self.valid_feed_mime_types:
            return True
        return False

    def _check_local_feed_magic(self, feed_path):
        """Checks the mimetype of a given local file by looking at the file
        header."""
        mimetype = magic.from_file(feed_path.encode('UTF-8'), mime=True)
        mimetype = mimetype.decode()
        mimetype = str(mimetype).split('; ')
        mimetype = mimetype[0]
        if mimetype in self.valid_feed_mime_types:
            return True
        msg = "Skipping %s %s." % (mimetype, feed_path)
        ResourceChecker._logger.warn(msg)
        return False
    
    def _check_local_image_mime_type(self, filename):
        sanity = self._check_image_mime_type(filename)
        return sanity
    
    def _check_remote_image_mime_type(self, filename):
        sanity = self._check_image_mime_type(filename)
        return sanity
    
    def _check_image_mime_type(self, filename):
        """Checks mime type guessed by filename."""
        mimetype = mimetypes.guess_type(filename, strict=False)[0]
        if mimetype.startswith("image/"):
            return True
        return False
    
    def _check_local_feed_bad_ends(self, feedPath):
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
    
    def _check_remote_existence(self, url):
        """
        Checks whether there exists a remote resource at the given path.

        >>> from ResourceChecker import ResourceChecker
        >>> resource_checker = ResourceChecker()
        >>> url = 'http://www.example.com/fakepath'
        >>> resource_checker._check_remote_existence(url)
        True
        >>> url = "http://www.asdfaljhfajefjksafbnlrnvlksvs.com/"
        >>> resource_checker._check_remote_existence(url)
        False
        """

        (netloc, path) = urlparse.urlparse(url)[1:3]
        conn = httplib.HTTPConnection(netloc)
        try:
            conn.request('HEAD', path)
        except socket.gaierror:
            return False # : [Errno -2] Name or service not known
        try:
            response = conn.getresponse()
        except AttributeError:
            return False # : 'NoneType' object has no attribute 'makefile'
        conn.close()
        return response.status in (200, 301, 302)
