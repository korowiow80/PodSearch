# AsyncNotifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import asyncore
import pyinotify

from FeedsDownloader import FeedsDownloader

class EventHandler(pyinotify.ProcessEvent):
    iDler = FeedsDownloader()
    
    def process_IN_CREATE(self, event):
        path = event.pathname
        print "IN_CREATE:", path
        self.iDler.handle_single_feed_list(path)

    def process_IN_MODIFY(self, event):
        path = event.pathname
        print "IN_MODIFY:", path
        self.iDler.handle_single_feed_list(path)

# Instanciate a new WatchManager (will be used to store watches).
wm = pyinotify.WatchManager()

# Add a new watch on /tmp for IN_CREATE and IN_MODIFY.
mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY # ignore errors, this works
feedRoot = '../../../static/1-FeedLists/'
wm.add_watch(feedRoot, mask, rec=True)

# Associate this WatchManager with a Notifier (will be used to report and
# process events).
notifier = pyinotify.AsyncNotifier(wm, EventHandler())

# Loop forever and handle events.
asyncore.loop()
