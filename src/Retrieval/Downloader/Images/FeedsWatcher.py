# AsyncNotifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import asyncore
import pyinotify

from ImagesDownloader import ImagesDownloader

class EventHandler(pyinotify.ProcessEvent):
    iDler = ImagesDownloader()
    
    def process_IN_CREATE(self, event):
        path = event.pathname
        print "IN_CREATE:", path
        self.iDler.handleFeed(path)

    def process_IN_MODIFY(self, event):
        path = event.pathname
        print "IN_MODIFY:", path
        self.iDler.handleFeed(path)

# Instanciate a new WatchManager (will be used to store watches).
wm = pyinotify.WatchManager()

# Add a new watch on /tmp for IN_CREATE and IN_MODIFY.
mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY # ignore errors, this works
feedRoot = '../../../static/2-Feeds/'
wm.add_watch(feedRoot, mask, rec=True)

# Associate this WatchManager with a Notifier (will be used to report and
# process events).
notifier = pyinotify.AsyncNotifier(wm, EventHandler())

# Loop forever and handle events.
asyncore.loop()
