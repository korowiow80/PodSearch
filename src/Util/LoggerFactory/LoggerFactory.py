"""Produces cheap loggers.

>>> import LoggerFactory import LoggerFactory
>>> logger = LoggerFactory().getLogger('MyClassName')
>>> logger.info('myMessage')
INFO: MyClassName: Initialized.
"""

import logging


class LoggerFactory:
    
    def __init__(self):
        pass
    
    def getLogger(self, name):        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logformat = '%(levelname)s: %(name)s: %(message)s'
        formatter = logging.Formatter(logformat)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
