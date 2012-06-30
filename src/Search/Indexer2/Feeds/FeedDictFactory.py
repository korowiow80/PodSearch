import xml.sax._exceptions
#import xml.dom.minidom

from bs4 import BeautifulSoup
import feedparser
#import speedparser

import DOM2Dict

class FeedDictFactory:
    
    _bs = BeautifulSoup()

    fields = ['author', 'title', 'description',
              #'image',
              #'language',
              #'link',
              #'summary',
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
                
            #===================================================================
            # self.feed = xml.dom.minidom.parse(feedPath)
            # self.feed = DOM2Dict.xmldom2dict(self.feed)
            # try:
            #   self.feed = self.feed['#document']['rss']['channel']
            # except (KeyError, TypeError):
            #    self.feed = None
            #    return False
            #===================================================================
            
            print "Parsed."
            
            return True
        except xml.sax._exceptions.SAXException:
            print "Aborted:", feedPath
            return False
    
    def getFeedDict(self, feedPath):
        
        if not self._parseFeed(feedPath):
            return
        
        feedDict = {}
        for fieldKey in self.fields:
            try:
                fieldValue = self.feed[fieldKey]
                try:
                    fieldValue = BeautifulSoup(fieldValue).get_text()
                    print fieldValue, fieldValue.encode("utf-8")
                    #fieldKey = fieldKey + '_s'
                    feedDict[fieldKey] = fieldValue #.encode("utf-8")
                except TypeError:
                    fieldValue = ""
            except KeyError:
                pass
        print "created feeddict"
        return feedDict
