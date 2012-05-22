import os
import errno
from urlparse import urlparse

import tldextract


class SpiderTool:
    
    projectRoot = "../../../"

    def __init__ (self):
        pass
        
    def derive (self, url):
        domain = self.getDomain(url)
        spiderName = self.getSpiderNameFromUrl(domain)
        directoryPath = self.getDirectoryPath(domain)
        feedListFilePath = self.getFeedListFilePath(domain)
        self.ensurePathExists(directoryPath)        
        baseUrl = self.getBaseUrl(url)
        return baseUrl, feedListFilePath, spiderName, directoryPath

    def makeSurePathExists(self, path):
        """Makes sure a given path exists.
        Tries to create the given path, handles eventual failure."""
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST: pass
            else: raise
        return

    def getAbsoluteUrl(self, url, baseUrl):
        if url.startswith('http'): return url
        else: return baseUrl + url

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
        if domain:
            spiderName = domain[0].upper() + domain.replace('.', '_')[1:]
        return spiderName

    def getDirectoryPath(self, domain):    
        """Derives the directory path from domain."""
        directoryPath = "../../../static/0-Directories/" + domain + "/"
        return directoryPath
    
    def getFeedListFilePath(self, domain):
        """Derives the feedlist path from a given domain and fullDomain."""
        feedListFilePath = "../../../static/1-Feedlists/" + domain + ".json"
        return feedListFilePath
