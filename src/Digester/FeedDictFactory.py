#import xml.dom.minidom
import subprocess
import sys
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
        proc = subprocess.Popen([sys.executable, '../Digester/FeedParserCli.py'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE)
        feedPath = feedPath.encode()
        stdout_value = proc.communicate(feedPath)[0]
        output = stdout_value
        
        return output
    
    def getFeedDict(self, feedPath):
        
        print(("Parsing:", feedPath))
        serializedFeed = self._parseFeed(feedPath)
        if not serializedFeed or str(serializedFeed) == "'null'" or len(serializedFeed) == 4:
            print('Parsing failed.')
            return
        print("Parsing succeeded.")
        
        serializedFeed = serializedFeed.decode("utf-8")

        print(("Deserializing."))
        deserializedFeed = json.loads(serializedFeed)
        print("Deserializing succeeded for with %s fields." % len(deserializedFeed))
        
        return deserializedFeed
