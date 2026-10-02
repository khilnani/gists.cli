#!/usr/bin/env python

from __future__ import print_function
import sys
from datetime import datetime

#-------------------------------------------

debugEnabled = False

def setDebug (debug):
  global debugEnabled
  debugEnabled = debug

def comment (obj):
  print('>> ' + str(obj))

def debug (obj):
  if debugEnabled:
    print('[' + str(datetime.now()) + ']: ' + str(obj))

def error (obj):
  print('ERROR: ' + str(obj))

def printDict (obj):
  for k,v in obj.items():
    print(k,v)
