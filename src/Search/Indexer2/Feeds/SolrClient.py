# -*- coding: utf-8 -*-

import time
import xml.parsers.expat

#from mysolr import Solr
#from Solr import Solr
import sunburnt

import PathTool
import FeedDictFactory

# create a connection to a solr server
#solr = Solr('http://localhost:8983/solr')
solr = sunburnt.SolrInterface("http://localhost:8983/solr/")

#===============================================================================
# documents = [
#   {'id' : 1,
#    'field1' : 'foo'
#   },
#   {'id' : 2,
#    'field2' : 'bar'
#   }
# ]
# solr.update(documents, 'json', commit=True)
#===============================================================================

_pt = PathTool.PathTool()
feeds = _pt.getFeedPaths()
lastCommitTime = 0
for feed in feeds:
    
    if not _pt.checkFeedPath(feed):
        print "Skipping:", feed
        continue
    
    try:
        feedDictFactory = FeedDictFactory.FeedDictFactory()
        feedDict = feedDictFactory.getFeedDict(feed)
        if feedDict != None and feedDict != {}:
            feedDict['id'] = _pt.getFeedId(feed)
            #feedDict = str(feedDict)
            #feedDict = "[" + feedDict + "]"
            #feedDict = [feedDict]
            #feedDict = feedDict.replace('\'', '\"')
            print "Indexing", feedDict
            #solr.update(feedDict, 'json', commit=False) # TODO do not commit every time
            #                    'json',
            solr.add(feedDict)
    except (xml.parsers.expat.ExpatError, ValueError):
        print "Failed:", feed
    
    now = time.time()
    if now - lastCommitTime >= 10:
        print "Committing..."
        solr.commit()
        print "Committed."
        lastCommitTime = now

#===============================================================================
# documents = [
#    {'id' : 1,
#     'field1' : 'foo'
#    },
#    {'id' : 2,
#     'field2' : 'bar'
#    }
# ]
# solr.update(documents, 'json', commit=True)
# 
# solr.commit()
#===============================================================================

print "b"