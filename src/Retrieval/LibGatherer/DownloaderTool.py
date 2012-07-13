import httplib
import threading
import Queue
import time

import httplib2

from UrlTool import UrlTool
from PathTool import PathTool


class DownloaderTool:
    """Commonly used tool that downloads resources of type feed or image."""
    
    def __init__(self):
        self.resources = []
        self._tdr = Threader()
        self._ut = UrlTool()
        self._pt = PathTool()
        self.last_download_timestamp = 0

    def download(self, resource_type, resource_url):
        """Downloads a resource of type feed or image by its URL."""
        
        if not self._ut.sanityCheckUrl(resource_url):
            return

        if resource_url.endswith('/'):
            resource_url = resource_url[:-1] 
        resource_target = self._pt.getRessourceTargetPath(resource_type, resource_url)
        base_path = self._pt.getBasePath(resource_target)
        print "DEBUG: Will download resource %s with target %s to location %s." % (resource_url, resource_target, base_path)
        
        self._pt.ensurePathExists(base_path)
        
        self.resources.append([resource_type, resource_url, resource_target])
        
        time_since_last_download = time.time() - self.last_download_timestamp 
        # download 300 files in parallel or how many ever we have every minute 
        if len(self.resources) <= 300 and time_since_last_download <= 60:
            return
        
        resources_tmp = self.resources
        self.resources = []
        self.last_download_timestamp = time.time()
        self._tdr.run_parallel_in_threads(_download, resources_tmp)

def _download(resource_type, resource_url, resource_target):
    """The method doing the actual downloading."""
    hl2 = httplib2.Http(cache=".cache", timeout=5)
    
    try:
        resp, content = hl2.request(resource_url)
        if  resp.fromcache:
            print "Cache contained a current version of %s %s." % (resource_type, resource_url)
        else:
            print "Downloaded %s from %s to %s." % (resource_type, resource_url, resource_target)
        with open(resource_target, 'w') as f:
            f.write(content)
    except (AttributeError, IOError, TypeError, UnicodeError, ValueError, \
            httplib.IncompleteRead, httplib.InvalidURL, httplib.BadStatusLine, \
            httplib2.RelativeURIError, httplib2.RedirectLimit, \
            httplib2.ServerNotFoundError, httplib2.SSLHandshakeError):
        # TODO actually do some error handling here
        pass


class Threader:
    """utility - spawn a thread to execute target for each args"""
    def __init__(self):
        pass
    
    def run_parallel_in_threads(self, target, args_list):
        """Runs a target method in multiple threads in parallel."""
        
        result = Queue.Queue()
        # wrapper to collect return value in a Queue
        def task_wrapper(*args):
            """I do not under stand this.""" #TODO
            result.put(target(*args))
        threads = [threading.Thread(target=task_wrapper, args=args) for args in args_list]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return result
