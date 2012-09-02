import time
import socket
import xml.parsers.expat

import sunburnt

from Resource.ResourceHelper import ResourceHelper
from Resource.ResourceChecker import ResourceChecker
from Util.PathTool import PathTool
from Digester.FeedDictFactory import FeedDictFactory

# create a connection to a solr server
try:
    solr = sunburnt.SolrInterface("http://localhost:8983/solr/")
except socket.error as e:
    print(e, "Is Solr started?")

_pt = PathTool.PathTool()
_rh = ResourceHelper()
_rc = ResourceChecker()
feeds = _rh.getAllFeedPaths()
for feed in feeds:

    print feed
    
    if not _rc.check_local_resource(feed, 'feed'):
        print("Skipping:", feed)
        continue
    
    try:
        feedDictFactory = FeedDictFactory()
        feedDict = feedDictFactory.getFeedDict(feed)
        if feedDict != None and feedDict != {}:
            feedDict['id'] = _pt.getFeedId(feed)
            print(("Indexing", feedDict))
            #feedDict['commitWithin']="10000"
            solr.add(feedDict, commit=True)
    except (xml.parsers.expat.ExpatError, ValueError):
        print(("Failed:", feed))

print("done")
