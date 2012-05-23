import os
import httplib
import threading
import Queue

import httplib2

from Scrapy.spiders.SpiderTool import SpiderTool


class DownloadTool:

    projectRoot = "../../../"

    def __init__ (self):
        self.ressources = []
        self.t = Threader()

    def download (self, ressourceType, ressourceUrl):
        if not self.sanityCheckUrl(ressourceUrl): return
        if ressourceUrl.endswith('/'): ressourceUrl = ressourceUrl[:-1] 
        ressourceTarget = self.getRessourceTarget(ressourceType, ressourceUrl)
        basePath = self.getBasePath(ressourceTarget)
        st = SpiderTool()
        st.makeSurePathExists(basePath)
        
        self.ressources.append([ressourceType, ressourceUrl, ressourceTarget])
        if len(self.ressources) <= 300: return
        
        ressourcesTmp = self.ressources
        self.ressource = []

        self.t.run_parallel_in_threads(_download, ressourcesTmp)
        
    def sanityCheckUrl (self, url):
        if not url: return False
        if url.endswith('://'): return False
        # skip dataUrls
        if url.startswith('data:'): return False

        # TODO do real url validation here ... like Django does
        return True

    def getRessourceTarget(self, ressourceType, ressourceUrl):
        if ressourceType == 'feed':
            ressourceTarget = self.getFeedFilePath(ressourceUrl)
        if ressourceType == 'image':
            ressourceTarget = self.getImageFilePath(ressourceUrl)        
        return ressourceTarget

    def getBasePath(self, ressourceTarget):
        basePath = os.path.dirname(ressourceTarget)
        return basePath

    def getImageFilePath(self, imageUrl):
        imagesPrefix = self.projectRoot + "web/img/"
        relativeRemoteLocation = self.getRelativePath(imageUrl)
        st = SpiderTool()
        domain = st.getDomain(imageUrl)        
        imageFilePath = imagesPrefix + domain + relativeRemoteLocation
        return imageFilePath

    def getFeedFilePath(self, feedUrl):
        feedsPrefix = self.projectRoot + "static/2-Feeds/"
        relativeRemoteLocation = self.getRelativePath(feedUrl)
        st = SpiderTool()
        domain = st.getDomain(feedUrl)
        feedFilePath = feedsPrefix + domain + relativeRemoteLocation        
        return feedFilePath

    def getRelativePath(self, url):
        if not url.startswith('http'): return url
        st = SpiderTool()
        baseUrl = st.getBaseUrl(url)
        relativePath = url[len(baseUrl):]
        return relativePath

def _download (ressourceType, ressourceUrl, ressourceTarget):
    # TODO multiprocess the actual downloading
    
    hl2 = httplib2.Http(cache = ".cache", timeout = 5)
    
    try:
        resp, content = hl2.request(ressourceUrl)
        if  resp.fromcache:
            print "Cache contained a current version of %s %s" % (ressourceType, ressourceUrl)
        else:
            print "Downloaded %s from %s to %s" % (ressourceType, ressourceUrl, ressourceTarget)
        with open(ressourceTarget, 'w') as f:
            f.write(content)
    except (IOError, httplib.InvalidURL, httplib.BadStatusLine, httplib2.ServerNotFoundError, httplib2.RelativeURIError, AttributeError, TypeError):
        pass

class Threader:
    
    # utility - spawn a thread to execute target for each args
    def run_parallel_in_threads(self, target, args_list):
        result = Queue.Queue()
        # wrapper to collect return value in a Queue
        def task_wrapper(*args):
            result.put(target(*args))
        threads = [threading.Thread(target=task_wrapper, args=args) for args in args_list]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return result
