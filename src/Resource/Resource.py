"""The resource object is the central data structure of PodSearch.

>>> from Resource import Resource
>>> feed = Resource("http://feeds.feedburner.com/cre-podcast", "feed")
>>> feed.get_absolute_url()
'http://feeds.feedburner.com/cre-podcast'
>>> feed.get_base_path()
'../../static/2-Feeds/fe/feeds.feedburner.com'
>>> feed.get_base_url()
'http://feeds.feedburner.com'
>>> feed.get_domain()
'feeds.feedburner.com'
>>> feed.get_filename()
'cre-podcast'
>>> feed.get_id()
'fe/feeds.feedburner.com/cre-podcast'
>>> feed.get_path()
'../../static/2-Feeds/fe/feeds.feedburner.com/cre-podcast'
>>> feed.get_relative_url()
'/cre-podcast'
>>> feed.get_spider_name()
>>> directory = Resource("http://podster.de/tag/system:all", "directory")
>>> directory.get_absolute_url()
'http://podster.de/tag/system:all'
>>> directory.get_base_path()
'../../static/1-Feedlists'
>>> directory.get_base_url()
'http://podster.de'
>>> directory.get_domain()
'podster.de'
>>> directory.get_filename()
'system:all'
>>> directory.get_id()
'static/1-Feedlists/podster.de.txt'
>>> directory.get_path()
'../../static/1-Feedlists/podster.de.txt'
>>> directory.get_relative_url()
'/tag/system:all'
>>> directory.get_spider_name()
'Podster_de'
"""

import os
import posixpath
import tldextract
from urlparse import urlparse

from Util.PathTool.PathTool import PathTool


class Resource:
    """Represents both an URL of a resource on a remote file system and a
    corresponding path to the local representation."""

    _pt = PathTool()

    def __init__(self, url, resource_type):
        self._url = ''
        self._set_url(url)
        self._type = ''
        self._id = ''
        self._path = ''
        self._set_type(resource_type)
    
    def _set_url(self, url):
        """Sets the url attribute of this resource."""
        self._url = url
    
    def _set_type(self, resource_type):
        """Sets the type attribute of this resource."""
        self._type = resource_type
        self._set_path()
        self._set_id()
        self._set_id()
        
    def _set_path(self):
        """Derives the download destination."""
        if self._type == "directory":
            self._set_feed_list_path()
        if self._type == "feed":
            self._set_feed_path()
        if self._type == "image":
            self._set_image_path()

    def _set_id(self):
        """Sets the _id of this resource relative to the corresponding resource
        directory."""
        new_id = self.get_path()

        new_id = new_id.lstrip('/.')
        while new_id.startswith('static/2-Feeds/'):
            new_id = new_id[len('static/2-Feeds/'):]
            new_id = new_id.lstrip('/.')
        
        new_id = new_id.rstrip('./')    # just to be sure
        
        self._id = new_id
    
    def _set_directory_path(self):
        """Derives the directory path from domain."""
        domain = self.get_domain()
        directories_path = self._pt.getDirectoriesPath()
        directory_path = directories_path + domain + "/"
        self._path = directory_path

    def _set_feed_list_path(self):
        """Derives the path of a feedlist from a given url."""
        domain = self.get_domain()
        feed_lists_path = self._pt.getFeedListsPath()
        #feed_lists_path = feed_lists_path[3:]
        # somehow we need to go up one level for the crawlers
        feed_list_path = feed_lists_path + domain + ".txt"
        self._path = feed_list_path

    def _set_feed_path(self):
        """Derives the path of a feed from a given url."""
        feeds_path = self._pt.getFeedsPath()
        remote_location = self.get_relative_url()
        domain = self.get_domain()
        prefix_folder = domain[:2] + "/"
        feed_file_path = feeds_path + prefix_folder + domain + remote_location
        self._path = feed_file_path
    
    def _set_image_path(self):
        """Derives the path of an image from a given url."""
        images_prefix = self._pt.getImagesPath()
        relative_remote_location = self.get_path()
        domain = self.get_domain()
        image_file_path = images_prefix + domain + relative_remote_location
        self._path = image_file_path

    def get_absolute_url(self):
        """Returns the absolute URL for an relative URL and a baseurl."""  
        if self._url.startswith('http'):
            return self._url
        else:
            absolute_url = self.get_base_url() + self.get_relative_url()
            return absolute_url

    def get_base_url(self):
        """Derives the base_url from a given url."""
        parse_result = urlparse(self._url)
        base_url = parse_result.scheme + '://' + parse_result.netloc
        return base_url

    def get_domain(self):
        """Extracts the full and the top-level domain from a given URL.
        By our convention, we skip the sub-domain, if it is 'www'."""
        extract = tldextract.extract(self._url)
        if extract.subdomain and extract.subdomain != 'www' and \
                extract.subdomain != 'api' and extract.subdomain != 'podcast':
            domain = ".".join(extract)
        else:
            domain = ".".join(extract[1:])
        return domain
    
    def get_relative_url(self):
        """Derives the filename from a given url."""
        if not self._url.startswith('http'):
            return self._url
        base_url = self.get_base_url()
        url = self.get_absolute_url()
        relative_url = url[len(base_url):]
        return relative_url
    
    def get_filename(self):
        """Derives the filename from a given URL."""
        parse_result = urlparse(self._url)
        remote_path = parse_result.path
        filename = posixpath.basename(remote_path)
        return filename
    
    def get_base_path(self):
        """TODO understand and document me!"""
        base_path = os.path.dirname(self.get_path())
        
        # reconstruct path if it does not end with an filename extension
        base_path_end = base_path.split('/')[-1]
        ressource_target_end = self.get_path().split('/')[-1]
        if base_path_end == ressource_target_end and \
           base_path[-1] != '/':
            base_path = os.sep.join(base_path.split('/')[:-1])
        
        return base_path
        
    def get_spider_name(self):
        """Derives the spider name from the given domain and fullDomain.
        By general convention the first letter of a class gets capitalized."""
        
        if self._type != 'directory':      # spiders are for directories, only.
            return
        # TODO split resource in two classes 'Feed' and 'Directory' 
        
        domain = self.get_domain()
        try:
            spider_name = domain[0].upper() + domain.replace('.', '_')[1:]
        finally:
            pass
        return spider_name
  
    def get_path(self):
        """Returns the _path attribute."""
        return self._path

    def get_id(self):
        """Returns the _id attribute."""
        return self._id
