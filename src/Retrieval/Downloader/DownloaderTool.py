import httplib
import threading
import Queue
import time

import httplib2

from Scrapy.spiders.SpiderTool import SpiderTool


class DownloaderTool:

    _projectRoot = "../../../"

    def __init__ (self):
        self.ressources = []
        self.t = Threader()
        self.st = SpiderTool()
        self.lastDownloadTimestamp = 0

    def download (self, ressourceType, ressourceUrl):
        if not self.sanityCheckUrl(ressourceUrl): return
        if ressourceUrl.endswith('/'): ressourceUrl = ressourceUrl[:-1] 
        ressourceTarget = self.getRessourceTargetPath(ressourceType, ressourceUrl)
        basePath = self.getBasePath(ressourceTarget)

        self.st.makeSurePathExists(basePath)
        
        self.ressources.append([ressourceType, ressourceUrl, ressourceTarget])
        timeSinceLastDownload = time.time() - self.lastDownloadTimestamp 
        # download 300 files in parallel or how many ever we have every minute 
        if len(self.ressources) <= 300 and timeSinceLastDownload <= 60:
            return
        
        ressourcesTmp = self.ressources
        self.ressources = []
        
        self.lastDownloadTimestamp = time.time()

        self.t.run_parallel_in_threads(_download, ressourcesTmp)

def _download (ressourceType, ressourceUrl, ressourceTarget): 
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
