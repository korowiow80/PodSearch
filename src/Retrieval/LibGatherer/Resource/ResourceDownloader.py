import httplib
import threading
import Queue
import time

import httplib2

from PathTool import PathTool
from ResourceChecker import ResourceChecker
from Resource import Resource
from ResourceHelper import ResourceHelper

class ResourceDownloader:
    """Commonly used tool that downloads resources."""
    
    def __init__(self):
        self.resources = []
        self._tdr = Threader()
        self._pt = PathTool()
        self._rc = ResourceChecker()
        self._rh = ResourceHelper()
        self.last_download_timestamp = 0

    def download(self, resource_type, resource_url):
        """Downloads a resource of type feed or image by its URL."""
        
        if not self._rc.checkRemoteResource(resource_type, resource_url):
            return

        resource = Resource(resource_url, resource_type)
        if resource.getAbsoluteUrl().endswith('/'):
            resource.setUrl(resource.getAbsoluteUrl()[:-1])
        resource_target = resource.getPath()
        base_path = resource.getBasePath()
        print "DEBUG: Will download resource %s with target %s to location %s." % (resource_url, resource_target, base_path)
        
        self._rh.ensurePathExists(base_path)
        
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
