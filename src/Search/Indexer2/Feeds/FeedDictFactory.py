#import xml.dom.minidom
import subprocess
import json

from bs4 import BeautifulSoup

#import DOM2Dict

class FeedDictFactory:
    
    _bs = BeautifulSoup()
    
    def __init__(self):
        pass
        
    def _parseFeed(self, feedPath):
        #output = subprocess.check_output(['ls', '-1'])
        #output = subprocess.check_output(['python', './FeedParserCli.py'])
        proc = subprocess.Popen(['python', 'FeedParserCli.py'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
        stdout_value = proc.communicate(feedPath)[0]
        output = stdout_value
        
        return output
    
    def getFeedDict(self, feedPath):
        
        print "Parsing:", feedPath
        feedDict = self._parseFeed(feedPath)
        if not feedDict or str(feedDict) == "'null'":
            return
        print "Parsed."
        
        # deserialize feed
        print feedDict
        
        print "Loading ..."
        feedDict = json.loads(feedDict)
        print "beacon"
        print "Loaded:", feedDict
        
        return feedDict
