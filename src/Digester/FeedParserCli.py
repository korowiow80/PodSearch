"""Wraps Feedparser and provides a CLI"""

import sys
import xml.sax._exceptions
import json

from bs4 import BeautifulSoup
import feedparser
from Util.LoggerFactory.LoggerFactory import LoggerFactory
#import speedparser

class FeedParserCli:
    
    _logger = LoggerFactory().getLogger('FeedParserCli')
    
    # http://packages.python.org/feedparser/reference.html
    
    fields = {
    'bozo':False,
    'bozo_exception':False,
    'encoding':False,
    'entries':{},
#===============================================================================
# entries[i].author
# entries[i].author_detail
# entries[i].author_detail.name
# entries[i].author_detail.href
# entries[i].author_detail.email
# entries[i].comments
# entries[i].content
# entries[i].content[j].value
# entries[i].content[j].type
# entries[i].content[j].language
# entries[i].content[j].base
# entries[i].contributors
# entries[i].contributors[j].name
# entries[i].contributors[j].href
# entries[i].contributors[j].email
# entries[i].created
# entries[i].created_parsed
# entries[i].enclosures
# entries[i].enclosures[j].href
# entries[i].enclosures[j].length
# entries[i].enclosures[j].type
# entries[i].expired
# entries[i].expired_parsed
# entries[i].id
# entries[i].license
# entries[i].link
# entries[i].links
# entries[i].links[j].rel
# entries[i].links[j].type
# entries[i].links[j].href
# entries[i].links[j].title
# entries[i].published
# entries[i].published_parsed
# entries[i].publisher
# entries[i].publisher_detail
# entries[i].publisher_detail.name
# entries[i].publisher_detail.href
# entries[i].publisher_detail.email
# entries[i].source
# entries[i].source.author
# entries[i].source.author_detail
# entries[i].source.contributors
# entries[i].source.icon
# entries[i].source.id
# entries[i].source.link
# entries[i].source.links
# entries[i].source.logo
# entries[i].source.rights
# entries[i].source.rights_detail
# entries[i].source.subtitle
# entries[i].source.subtitle_detail
# entries[i].source.title
# entries[i].source.title_detail
# entries[i].source.updated
# entries[i].source.updated_parsed
# entries[i].summary
# entries[i].summary_detail
# entries[i].summary_detail.value
# entries[i].summary_detail.type
# entries[i].summary_detail.language
# entries[i].summary_detail.base
# entries[i].tags
# entries[i].tags[j].term
# entries[i].tags[j].scheme
# entries[i].tags[j].label
# entries[i].title
# entries[i].title_detail
# entries[i].title_detail.value
# entries[i].title_detail.type
# entries[i].title_detail.language
# entries[i].title_detail.base
# entries[i].updated
# entries[i].updated_parsed
# entries[i].vcard
# entries[i].xfn
# entries[i].xfn[j].relationships
# entries[i].xfn[j].href
# entries[i].xfn[j].name
#===============================================================================
    'etag':False,
    'feed':{
        'author':False,
        'author_detail':{
             'name', 'href', 'email'
        },
        'cloud': {
              'domain':False, 'port':False, 'path':False, 'registerProcedure':False, 'protocol':False,
              'contributors': {
                  'name', 'href', 'email', 'docs', 'errorreportsto'
              }
        },
        'generator':False,
        'generator_detail': {
             'name',
             'href',
             'version',
         },
        'icon':False,
        'id':False,
        'image': {
            'href', 'link', 'width', 'height', 'description'
        }
    }
#===============================================================================
# feed.info
# feed.info_detail
# feed.info_detail.value
# feed.info_detail.type
# feed.info_detail.language
# feed.info_detail.base
# feed.language
# feed.license
# feed.link
# feed.links
# feed.links[i].rel
# feed.links[i].type
# feed.links[i].href
# feed.links[i].title
# feed.logo
# feed.published
# feed.published_parsed
# feed.publisher
# feed.publisher_detail
# feed.publisher_detail.name
# feed.publisher_detail.href
# feed.publisher_detail.email
# feed.rights
# feed.rights_detail
# feed.rights_detail.value
# feed.rights_detail.type
# feed.rights_detail.language
# feed.rights_detail.base
# feed.subtitle
# feed.subtitle_detail
# feed.subtitle_detail.value
# feed.subtitle_detail.type
# feed.subtitle_detail.language
# feed.subtitle_detail.base
# feed.tags
# feed.tags[i].term
# feed.tags[i].scheme
# feed.tags[i].label
# feed.textinput
# feed.textinput.title
# feed.textinput.link
# feed.textinput.name
# feed.textinput.description
# feed.title
# feed.title_detail
# feed.title_detail.value
# feed.title_detail.type
# feed.title_detail.language
# feed.title_detail.base
# feed.ttl
# feed.updated
# feed.updated_parsed
# headers
# href
# modified
# namespaces
# status
# version
#===============================================================================
}
    
    dynamicFields = ['author',
                     'contributors',
                     'docs',
                     'errorreportsto',
                     'generator',
                     'title',
                     'description',
                     'image',
                     'language',
                     'link',
                     'summary',
                     'itunes:explicit',
                     'itunes:subtitle',
                     'itunes:summary',
                     'itunes:subtitle',
                     'updated',
                     'updated_parsed',
                     'headers',
                     'href',
                     'modified',
                     'namespaces',
                     'status',
                     'version',
                     'encoding',
                     'etag'
                     ]
    
    def __init__(self):
        pass
    
    def run(self):
        
        while True:
            feedPath = sys.stdin.readline()
            if not feedPath:
                break
            feed = self._parseFeed(feedPath)

            #feedDict = self.createFeedDict(feed)
            feedDict = self.createFeedDictRecursive(feed, None, self.fields)

            out = json.dumps(feedDict)
            sys.stdout.write(out)
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
    
    def createFeedDictRecursive (self, feed, root, fields):
        feedDict = {}
        self._logger.debug('root0: ' + str(root))
        if root:
            fields = fields[root]

        for fieldKey in fields:
            try:
                fields = self.fields[fieldKey] # 'encoding':False
                root += fieldKey
                self._logger.debug('root1: ' + str(root))
                feedDict += self.createFeedDictRecursive(feed, root, fields)
            except TypeError:
                try:
                    # leaf
                    feedDict += feed[root]
                except KeyError:
                    self._logger.debug('no such field ' + str(root))
                    pass
                
                if root:
                    feedDict[root] += feed[root]

        self._logger.debug(feedDict)
        return feedDict

    def createFeedDict (self, feed):
        
        feedDict = {}
        for fieldKey in self.dynamicFields:
            try:
                fieldValue = feed[fieldKey]
                try:
                    fieldKey = fieldKey + '_s' # lets assume all fields are dynamic
                    fieldValue = BeautifulSoup(fieldValue).get_text()
                    fieldValue = ' '.join(fieldValue.split())
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
