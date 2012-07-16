"""Wraps Feedparser and provides a CLI"""

import sys
import xml.sax._exceptions
import json

from bs4 import BeautifulSoup
import feedparser
#import speedparser

class FeedParserCli:
    
    fields = ['author', 'title', 'description']

    dynamicFields = ['image', 'language', 'link', 'summary',
                     'itunes:explicit', 'itunes:subtitle', 'itunes:summary', 'itunes:subtitle']
    
    def __init__(self):
        pass
    
    def run(self):
        
        while True:
            feedPath = sys.stdin.readline()
            if not feedPath:
                break

            feed = self._parseFeed(feedPath)

            feedDict = self.createFeedDict(feed)
            
            sys.stdout.write(json.dumps(feedDict))
            sys.stdout.flush()

    def _parseFeed (self, feedPath):      
        try:    
            #feed = speedparser.parse(feedPath)['feed']
            feed = feedparser.parse(feedPath)
            try:
                feed = feed['feed']
            except (KeyError, TypeError):
                return False

        except xml.sax._exceptions.SAXException:
            sys.stderr.write("Aborted.")
            sys.stderr.flush()
            return False
        
        return feed

    def createFeedDict (self, feed):
        
        feedDict = {}
        for fieldKey in self.fields + self.dynamicFields:
            try:
                fieldValue = feed[fieldKey]
                try:
                    fieldValue = BeautifulSoup(fieldValue).get_text()
                    if fieldKey in self.dynamicFields:
                        fieldKey = fieldKey + '_s'
                    feedDict[fieldKey] = fieldValue
                except TypeError:
                    fieldValue = ""
            except (KeyError, TypeError):
                pass
        if feedDict == {}:
            return
        return feedDict
    
    
if __name__ == '__main__':
    fpcli = FeedParserCli()
    fpcli.run()