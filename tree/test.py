#encoding: utf-8
import time
import sys
import requests
import json
from file import *
reload(sys)
sys.setdefaultencoding('utf-8')

nodes = read_file(NODE_FILENAME)
for i in nodes:
    try:
        for temp in i['student']:
            temp['value'] = '师->生'
    except KeyError:
        print 'error'
write_file(NODE_FILENAME,nodes)
print 111
