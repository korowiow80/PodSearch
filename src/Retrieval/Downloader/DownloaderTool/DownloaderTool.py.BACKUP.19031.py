import httplib
import threading
import Queue
import time

import httplib2

from UrlTool import UrlTool
from PathTool import PathTool


class DownloaderTool:

    def __init__ (self):
        self.resources = []
        self.t = Threader()
        self._ut = UrlTool()
        self._pt = PathTool()
        self.lastDownloadTimestamp = 0

    def download (self, resourceType, resourceUrl):
        if not self._ut.sanityCheckUrl(resourceUrl): return

        if resourceUrl.endswith('/'): resourceUrl = resourceUrl[:-1] 
        resourceTarget = self._pt.getRessourceTargetPath(resourceType, resourceUrl)
        basePath = self._pt.getBasePath(resourceTarget)
        print "DEBUG: Will download resource %s with target %s to location %s." % (resourceUrl, resourceTarget, basePath)
        
        self._pt.ensurePathExists(basePath)
        
        self.resources.append([resourceType, resourceUrl, resourceTarget])
        
        timeSinceLastDownload = time.time() - self.lastDownloadTimestamp 
        # download 300 files in parallel or how many ever we have every minute 
        if len(self.resources) <= 300 and timeSinceLastDownload <= 60:
            return
        
        resourcesTmp = self.resources
        self.resources = []
        self.lastDownloadTimestamp = time.time()
        self.t.run_parallel_in_threads(_download, resourcesTmp)

def _download (resourceType, resourceUrl, resourceTarget): 
    hl2 = httplib2.Http(cache = ".cache", timeout = 5)
    
    try:
        resp, content = hl2.request(resourceUrl)
        if  resp.fromcache:
<<<<<<< HEAD
            print "Cache contained a current version of %s %s." % (resourceType, resourceUrl)
        else:
            print "Downloaded %s from %s to %s." % (resourceType, resourceUrl, resourceTarget)
        with open(resourceTarget, 'w') as f:
            f.write(content)
    except (AttributeError, IOError, TypeError, UnicodeError, ValueError,  \
            httplib.IncompleteRead, httplib.InvalidURL, httplib.BadStatusLine, \
=======
            print "Cache contained a current version of %s %s." % (ressourceType, ressourceUrl)
        else:
            print "Downloaded %s from %s to %s." % (ressourceType, ressourceUrl, ressourceTarget)
        with open(ressourceTarget, 'w') as f:
            f.write(content)
    except (AttributeError, IOError, TypeError, UnicodeError, ValueError,  \
            httplib.InvalidURL, httplib.BadStatusLine, \
>>>>>>> 27e218d... Hopefully fixed the issue with paths derived from strange filenames, now.
            httplib2.RelativeURIError, httplib2.RedirectLimit, \
            httplib2.ServerNotFoundError):
        # TODO actually do some error handling here
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
