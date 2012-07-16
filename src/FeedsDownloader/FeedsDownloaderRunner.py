import os
import json

from FeedsDownloader import FeedsDownloader
from Util.PathTool import PathTool
from Resource.ResourceHelper import ResourceHelper
from Util.LoggerFactory.LoggerFactory import LoggerFactory

class FeedsDownloaderRunner:
    """Runs the DownloadTool with URLs of feeds, gathered from the feed lists."""

    _fd = FeedsDownloader()
    _pt = PathTool.PathTool()
    _rh = ResourceHelper()
    _logger = LoggerFactory().getLogger('FeedsDownloaderRunner')
    
    def __init__(self):
        FeedsDownloaderRunner._logger.debug('Initialized.')

    def run(self):
        """Runs downloads of all feeds."""
        feed_urls = self.get_all_feed_urls()
        self.download_feeds(feed_urls)
    
    def handle_single_feed_list(self, feed_list_path):
        """Runs downloads for one feed list."""
        feed_urls = self.get_feed_urls_from_feed_list(feed_list_path)
        self.download_feeds(feed_urls)
        
    def download_feeds(self, feed_urls):
        """Runs downloads of specified feeds."""
        FeedsDownloaderRunner._logger.info('Starting downloads for %s feeds.' % len(feed_urls))
        self._fd.downloadFeeds(feed_urls)
        FeedsDownloaderRunner._logger.info('FeedsDownloaderRunner: INFO: Done.')
        
    def get_all_feed_urls(self):
        """Collects all URLs of feeds from the lists of feeds."""
        
        feed_lists_directory = self._pt.getFeedListsPath()
        relative_feed_lists_paths = os.listdir(feed_lists_directory)
        all_feed_urls = []
        for relative_feed_list_path in relative_feed_lists_paths:
            if relative_feed_list_path == 'podster.list':
                continue
            if relative_feed_list_path == 'podcast.com.json':
                continue
            some_feed_urls = self.get_feed_urls_from_feed_list(relative_feed_list_path)
            for feed_url in some_feed_urls:
                feed_url = self._rh.stripWhitespace(feed_url)
                all_feed_urls.append(feed_url)
        return all_feed_urls
    
    def get_feed_urls_from_feed_list(self, feed_list_path):
        """Parses all feed urls from download_feeds list of feeds by its path."""
        
        feed_lists_directory = self._pt.getFeedListsPath()
        absolute_feed_list_path = feed_lists_directory + feed_list_path
        if feed_list_path.endswith('.json'):
            feed_urls = self.get_feed_urls_from_json_feed_list(absolute_feed_list_path)
        else:
            feed_urls = self.get_feed_urls_from_text_feed_list(absolute_feed_list_path)
        return feed_urls
        
    def get_feed_urls_from_json_feed_list(self, absolute_feed_list_path):
        feed_urls = []
        print(absolute_feed_list_path)
        with open(absolute_feed_list_path, 'r') as f:
            contents = f.read()
            feed_items = json.loads(contents)
            for feed_item in feed_items:
                feed_urls.append(feed_item['link'])
        return feed_urls

    def get_feed_urls_from_text_feed_list(self, absolute_feed_list_path):
        feed_urls = []
        with open(absolute_feed_list_path, 'r') as f:
            for line in f.readlines():
                feed_urls.append(self._rh.stripWhitespace(line))
        return feed_urls

if __name__ == '__main__':
    FDR = FeedsDownloaderRunner()
    FDR.run()
