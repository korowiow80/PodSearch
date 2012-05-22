#! /usr/bin/python

import errno
import os

# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python

class Mkdir_p:

    def __init__ (self):
        pass

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST:
                pass
            else: raise
