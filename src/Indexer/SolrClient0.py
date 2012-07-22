# -*- coding: utf-8 -*-

import time
import socket
import xml.parsers.expat

#import sunburnt
from mysolr import Solr

from Resource.ResourceHelper import ResourceHelper
from Resource.Resource import Resource
from Util.PathTool import PathTool
from Digester.FeedDictFactory import FeedDictFactory

solrBase = "http://localhost:8983/solr/"
updateUrl = solrBase + 'update/'

solr = Solr(solrBase)

_pt = PathTool.PathTool()
_rh = ResourceHelper()
feeds = _rh.getAllFeedPaths()
for feed in feeds:   
    try:
        feedDictFactory = FeedDictFactory()
        feedDict = feedDictFactory.getFeedDict(feed)
        if feedDict != None and feedDict != {}:
            feedDict['id'] = Resource(feed, 'feed').getId()
            print(feedDict['id'])
            print("Indexing", feedDict)
            
            solr.update([feedDict], 'json', commit=True)
            print('Indexed.')
    except (xml.parsers.expat.ExpatError, ValueError):
        print(("Failed:", feed))

print("done")
