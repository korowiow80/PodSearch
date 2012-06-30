import urlparse
import tldextract
import magic
import mimetypes
import posixpath
import urllib

class UrlTool:
    
    def getAbsoluteUrl(self, relativeUrl, baseUrl):
        """Returns the absolute URL for an relative URL and a baseurl."""  
        if relativeUrl.startswith('http'): return relativeUrl
        else: return baseUrl + relativeUrl
    
    def getBaseUrl(self, url):
        """Derives the baseUrl from a given url."""
        o = urlparse.urlparse(url)
        baseUrl = o.scheme + '://' + o.netloc
        return baseUrl

    def getRelativeUrl(self, url):
        """Derives the filename from a given url."""
        if not url.startswith('http'): return url
        baseUrl = self.getBaseUrl(url)
        relativeUrl = url[len(baseUrl):]
        return relativeUrl

    def getDomain(self, url):
        """Extracts the full and the top-level domain from a given URL.
        By our convention, we skip the sub-domain, if it is 'www'."""
        extract = tldextract.extract(url)
        if extract.subdomain and extract.subdomain != 'www':
            domain = ".".join(extract)
        else:
            domain = ".".join(extract[1:])
        return domain
    
    def getFilename(self, url):
        """Derives the filename from a given URL."""
        urlParts = urlparse.urlsplit(url)
        remotePath = urlParts.path
        filename = posixpath.basename(remotePath)
        return filename

    def getSpiderName(self, url):
        """Derives the spider name from the given domain and fullDomain.
        By general convention the first letter of a class gets capitalized."""
        domain = self.getDomain(url)
        try:
            spiderName = domain[0].upper() + domain.replace('.', '_')[1:]
        finally:
            return spiderName

    def sanityCheckRessource(self, ressourceType, url):
        """Checks the URL for sanity according to the ressourceType.
        Returns True if the URL is sane for this ressourceType, otherwise
        False."""
        if not url: return False
        if not ressourceType: return False #TODO we should raise here

        if not self.sanityCheckUrl(url): return False
        
        if ressourceType == 'feed': sanity = self.sanityCheckFeedUrl(url)
        if ressourceType == 'image': sanity = self.sanityCheckImageUrl(url)

        return sanity
    
    def sanityCheckUrl(self, url):
        """Checks an URL for sanity. Returns True if the URL is sane, otherwise
        False."""

        if url.endswith('://'): return False

        # TODO do real url validation here ... like Django does
        
        return True
        
    def sanityCheckImageUrl(self, url):
        """Checks an image URL for sanity. Returns True if the URL is sane,
        otherwise False."""
        
        # We skip dataUrls
        if url.startswith('data:'):
            return False
        
        sanity = self.checkImageMimeType(url)

        return sanity
    
    def sanityCheckFeedUrl(self, url):
        """Checks an URL of a feed for sanity. Returns True if the URL is sane,
        otherwise False."""

        if self.checkFeedUrlFileType(url):
            return True

        feedFilename = self.getFilename(url)
        if not self._pt.checkFeedMimeType(feedFilename):
            return False
        
        sanity = self.checkFeedFileType(url)
        if not sanity:
            print "UrlTool: WARN: Did not recognize mime media type of feed %s." % (url)
        return sanity
    
    def checkFeedUrlFileType(self, url):
        # Google's Feedburner always does the right thing.^tm
        if url.startswith('http://feeds.feedburner.com/'):
            return True
        
        # If the URL seems sane, we believe that, too.
        if url.endswith('/rss'):
            return True
        
        return False
