#! /bin/python

import os
import errno

import tldextract


class SpiderTool:

    def __init__ (self):
        pass
        
    def derive (self, url):        
        # extract fullDomain from URL
        extract = tldextract.extract(url)
        if extract.subdomain:
            fullDomain = ".".join(extract)
            domainTld = ".".join(extract[1:])
        else:
            fullDomain = ".".join(extract[1:])
            domainTld = None
        
        # derive name from TLD
        # by general convention the first letter of a class gets capitalized
        # by our convention, we skip the sub-domain, if it is 'www'
        if domainTld:
            name = domainTld[0].upper() + domainTld.replace('.', '_')[1:]
        else:
            name = fullDomain[0].upper() + fullDomain.replace('.', '_')[1:]
        
        # derive prefix from domain
        # by convention we skip the www
        if domainTld:
            prefix = "../../static/0-Directories/" + domainTld + "/"
        else:
            prefix = "../../static/0-Directories/" + fullDomain + "/"
        
        # make sure the prefix exists
        try:
            os.makedirs(prefix)
        except OSError as exc:
            if exc.errno == errno.EEXIST: pass
            else: raise
            
        return name, prefix