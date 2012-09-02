import urllib2
import threading
from multiprocessing import Queue
import time

import httplib2

from Resource.Resource import Resource
from Resource.ResourceChecker import ResourceChecker
from Resource.ResourceHelper import ResourceHelper
from Util.PathTool import PathTool
from Util.LoggerFactory.LoggerFactory import LoggerFactory
from Util.Decoder.Decoder import Decoder

class ResourceDownloader:
    """Commonly used tool that downloads resources."""
    
    _logger = LoggerFactory().getLogger('RessourceDownloader')
    _resources = []
    _downloadedResources = []
    
    def __init__(self):
        self._tdr = Threader()
        self._pt = PathTool.PathTool()
        self._rc = ResourceChecker()
        self._rh = ResourceHelper()
        self.last_download_timestamp = 0

    def download(self, resource_type, resource_url):
        """Downloads a resource of type feed or image by its URL."""
        
        if not self._rc.check_remote_resource(resource_type, resource_url):
            return

        resource = Resource(resource_url, resource_type)
        if resource.get_absolute_url().endswith('/'):
            resource._set_url(resource.get_absolute_url()[:-1])
        resource_target = resource.get_path()
        base_path = resource.get_base_path()
        msg = 'DEBUG: Will download resource %s with target %s to location %s.' \
              % (resource_url, resource_target, base_path)
        ResourceDownloader._logger.info(msg)
        
        self._rh.ensurePathExists(base_path)
        
        args = [resource_type, resource_url, resource_target]
        
        duplicate_found = False
        if not duplicate_found:
            for dedup_args in ResourceDownloader._resources:
                if dedup_args[2] == args[2]:
                    duplicate_found = True
                    break
        if not duplicate_found:
            for dedup_args in ResourceDownloader._downloadedResources:
                if dedup_args[2] == args[2]:
                    duplicate_found = True
                    break
        if not duplicate_found:
            ResourceDownloader._resources.append(args)
        
        time_since_last_download = time.time() - self.last_download_timestamp 
        # download 300 files in parallel or how many ever we have every minute
        if len(ResourceDownloader._resources) <= 1000 and time_since_last_download <= 60: # TODO
            return
        
        resources_tmp = ResourceDownloader._resources
        ResourceDownloader._resources = []
        ResourceDownloader._downloadedResources = ResourceDownloader._downloadedResources + resources_tmp
        self.last_download_timestamp = time.time()
        self._tdr.run_parallel_in_threads(_download, resources_tmp)

def _download(resource_type, resource_url, resource_target):
    """Does the actual downloading."""
    if resource_type == 'feed':
        _hl2 = httplib2.Http(cache="../../cache/httplib2/feed", timeout=5)
    if resource_type == '':
        _hl2 = httplib2.Http(cache="../../cache/httplib2/image", timeout=5)
    if not _hl2:
        print resource_type
        raise # not yet implemented
    _logger = LoggerFactory().getLogger('_download')
    try:
        resp, content = _hl2.request(resource_url)
        if  resp.fromcache:
            msg = "Cache contained a current version of %s %s." % (resource_type, resource_url)
            _logger.info(msg)
        else:
            msg = "Downloaded %s from %s to %s." % (resource_type, resource_url, resource_target)
            _logger.info(msg)
            with open(resource_target, 'w') as f:
                content = Decoder().decode(content)
                f.write(content)
    except (AttributeError, IOError, TypeError, UnicodeError, ValueError, \
            urllib2.IncompleteRead, urllib2.InvalidURL, urllib2.BadStatusLine, \
            httplib2.RelativeURIError, httplib2.RedirectLimit, \
            httplib2.ServerNotFoundError) as e:
        # TODO actually do some error handling here
        print(e)
        #pass


class Threader:
    """Spawns a thread to execute target for each args"""
    def __init__(self):
        pass
    
    def run_parallel_in_threads(self, target, args_list):
        """Runs a target method in multiple threads in parallel."""
        
        # deduplication
        # http://stackoverflow.com/a/1143432
        args_list = dict((x[0], x) for x in args_list).values()
        
        result = queue.Queue()
        # wrapper to collect return value in a Queue
        def task_wrapper(*args):
            """I do not understand this.""" #TODO
            result.put(target(*args))
        threads = [threading.Thread(target=task_wrapper, args=args) for args in args_list]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return result
