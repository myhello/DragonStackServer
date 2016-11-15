'''
Created on 2016.3.6

@author: sixu
'''

import logging
import logging.handlers
        
class MyLog(object):
    '''
    classdocs
    '''

    def __init__(self,message):
        '''
        Constructor
        '''
        
        print "server.log"
        LOG_FILE = 'Log/server.log'

        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)  
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

        formatter = logging.Formatter(fmt)   
        handler.setFormatter(formatter)      

        logger = logging.getLogger('server')    
        logger.addHandler(handler)           
        logger.setLevel(logging.DEBUG)

        logger.info(message)
        #logger.debug(message)
        
