import urlparse
import tldextract
import magic
import mimetypes
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
        Returns True if the URL is sane for this ressourceType and False,
        otherwise."""
        if not url: return False
        if not ressourceType: return False #TODO we should raise here

        if not self.sanityCheckUrl(url): return False
        
        if ressourceType == 'feed': sanity = self.sanityCheckFeedUrl(url)
        if ressourceType == 'image': sanity = self.sanityCheckImageUrl(url)

        return sanity
    
    def sanityCheckUrl(self, url):
        """Checks an URL for sanity. Returns True if the URL is sane, False,
        otherwise."""

        if url.endswith('://'): return False

        # TODO do real url validation here ... like Django does
        
        return True
        
    def sanityCheckImageUrl(self, url):
        """Checks an image URL for sanity. Returns True if the URL is sane, False,
        otherwise."""
        
        # We skip dataUrls
        if url.startswith('data:'): return False
        
        sanity = self.checkImageMimeType(url)

        return sanity
    
    def sanityCheckFeedUrl(self, url):
        """Checks an feed URL for sanity. Returns True if the URL is sane, False,
        otherwise."""
                
        sanity = self.checkFeedMimeType(url)

        return sanity
    
    def checkFeedMimeType(self, url):
        
        # Google's Feedburner always does the right thing.^tm
        if url.startswith('http://feeds.feedburner.com/'): return True
        
        # If the URL seems sane, we believe that, too.
        if url.endswith('/rss'): return True
        
        # really valid is only 'application/rss+xml'.
        # see http://stackoverflow.com/questions/595616/what-is-the-correct-mime-type-to-use-for-an-rss-feed
        validFeedMimeTypes = ['application/rss+xml',
                              'application/xml',
                              'text/xml']
        
        # Try accepting using included batteries
        miMimetype, encoding = mimetypes.guess_type(url, strict=False)
        if miMimetype in validFeedMimeTypes:
            return True
        
        # Try accepting using magic
        filename, headers = urllib.urlretrieve(url, 'tmp')

        mime = magic.open(magic.MAGIC_MIME)
        mime.load()
        maMimetype = mime.file(filename)

        maMimetype = maMimetype.split('; ')[0]
        if maMimetype in validFeedMimeTypes:
            #print "UrlTool: INFO: Recognized mime media type of feed %s as %s." % (url, maMimetype)
            return True

        print "UrlTool: WARN: Did not recognize mime media type of feed %s, appearing to be %s or %s." % (url, miMimetype, maMimetype)
            
        return False
