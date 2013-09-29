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

if sys.argv[-1] in ('debug'):
  enabled = True
  del sys.argv[-1]
