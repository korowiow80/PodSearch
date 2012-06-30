import xml.sax._exceptions
#import xml.dom.minidom

from bs4 import BeautifulSoup
import feedparser
#import speedparser

import DOM2Dict

class FeedDictFactory:
    
    _bs = BeautifulSoup()

    fields = ['author', 'title', 'description']

    dynamicFields = ['image', 'language', 'link', 'summary',
                     'itunes:explicit', 'itunes:subtitle', 'itunes:summary', 'itunes:subtitle']
    
    def __init__(self):
        pass
        
    def _parseFeed(self, feedPath):
        
        try:
            print "Parsing:", feedPath
            
            #self.feed = speedparser.parse(feedPath)['feed']
            self.feed = feedparser.parse(feedPath)
            try:
                self.feed = self.feed['feed']
            except (KeyError, TypeError):
                return False

            print "Parsed."
            
            return True
        except xml.sax._exceptions.SAXException:
            print "Aborted."
            return False
    
    def getFeedDict(self, feedPath):
        
        if not self._parseFeed(feedPath):
            return
        
        feedDict = {}
        for fieldKey in self.fields + self.dynamicFields:
            try:
                fieldValue = self.feed[fieldKey]
                try:
                    fieldValue = BeautifulSoup(fieldValue).get_text()
                    if fieldKey in self.dynamicFields:
                        fieldKey = fieldKey + '_s'
                    feedDict[fieldKey] = fieldValue
                except TypeError:
                    fieldValue = ""
            except KeyError:
                pass
        return feedDict
