import urlparse
import tldextract


class UrlTool:
    def getAbsoluteUrl(self, relativeUrl, baseUrl):
        """Returns the absolute URL for an relative URL and a baseurl."""  
        if relativeUrl.startswith('http'): return relativeUrl
        else: return baseUrl + relativeUrl
    
    def getBaseUrl(self, url):
        """Derives the baseUrl from a given url."""
        o = urlparse(url)
        baseUrl = o.scheme + '://' + o.netloc
        return baseUrl
    
    def getDomain(self, url):
        """Extracts the full and the top-level domain from a given URL.
        By our convention, we skip the sub-domain, if it is 'www'."""
        extract = tldextract.extract(url)
        if extract.subdomain and extract.subdomain != 'www':
            domain = ".".join(extract)
        else:
            domain = ".".join(extract[1:])
        return domain
    
    def getSpiderNameFromUrl(self, domain):
        """Derives the spider name from the given domain and fullDomain.
        By general convention the first letter of a class gets capitalized."""
        try:
            spiderName = domain[0].upper() + domain.replace('.', '_')[1:]
        finally:
            return spiderName
    
    def sanityCheckUrl (self, url):
        """Checks an URL for sanity. Returns True if the URL ist sane, False,
        otherwise."""
        if not url: return False
        
        if url.endswith('://'): return False
        # skip dataUrls
        if url.startswith('data:'): return False

        # TODO do real url validation here ... like Django does
        return True
