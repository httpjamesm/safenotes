#!/usr/bin/python

import json

try:
    with open('settings.json','r') as json_file:
        configdata = json.load(json_file)
        #print('congidata loaded')
except Exception as e:
    print(e)


