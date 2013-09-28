#!/usr/bin/env python

import sys
from datetime import datetime

#-------------------------------------------

enabled = False
def comment (obj):
  print '>> ' + str(obj)

def debug (obj):
  if enabled:
    print '[' + str(datetime.now()) + ']: ' + str(obj)

for arg in sys.argv:
  if arg in ('debug'):
    enabled = True
