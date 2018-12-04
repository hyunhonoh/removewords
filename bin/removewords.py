#!/bin/python
#-*- coding: utf-8 -*-
import splunk.Intersplunk, splunk.util
import itertools
import exec_anaconda
exec_anaconda.exec_anaconda()

import numpy as np
import pandas as pd
import re, os, sys
import logging, logging.handlers

###
### Splunk logging setup
###
def setup_logging():
    logger = logging.getLogger('splunk.removewords')
    SPLUNK_HOME = os.environ['SPLUNK_HOME']

    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = "removewords.log"
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
    splunk_log_handler = logging.handlers.RotatingFileHandler(os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger


def removewords(results, settings):
    SPLUNK_HOME = os.environ['SPLUNK_HOME']
    ### 지우는 파일 목록
    ###
    ### header : 삭제여부, body_split
    ### 예시   : 'o', '삭제대상'
    REMOVEWORDS = os.path.join(SPLUNK_HOME, 'etc', 'apps', 'removewords', 'lookups', 'removewords.csv')

    try:
        fields, argvals = splunk.Intersplunk.getKeywordsAndOptions()
        df = pd.read_csv(REMOVEWORDS)
        resultsplit=[]
        for r in results:
            for f in fields:
                if f in r:           
                    delword = df[(df['삭제여부']=='o') & (df['body_split']==r[f])]
                    
                    if(delword['body_split'].count()):
                        r['removewords']="del"
                    else:
                        r['removewords']="keep"

        splunk.Intersplunk.outputResults(results)
    except:
        import traceback
        stack =  traceback.format_exc()
        results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

logger = setup_logging()
results, dummyresults, settings = splunk.Intersplunk.getOrganizedResults()
results = removewords(results, settings)

