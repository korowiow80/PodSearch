# -*- coding: utf-8 -*-

import time
import xml.parsers.expat

import sunburnt

import PathTool
import FeedDictFactory

# create a connection to a solr server
solr = sunburnt.SolrInterface("http://localhost:8983/solr/")

_pt = PathTool.PathTool()
feeds = _pt.getFeedPaths()
for feed in feeds:
    
    if not _pt.checkFeedPath(feed):
        print(("Skipping:", feed))
        continue
    
    try:
        feedDictFactory = FeedDictFactory.FeedDictFactory()
        feedDict = feedDictFactory.getFeedDict(feed)
        if feedDict != None and feedDict != {}:
            feedDict['id'] = _pt.getFeedId(feed)
            print(("Indexing", feedDict))
            #feedDict['commitWithin']="10000"
            solr.add(feedDict, commit=True)
    except (xml.parsers.expat.ExpatError, ValueError):
        print(("Failed:", feed))

print("done")
