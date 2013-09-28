#!/usr/bin/env python

import sys

#-------------------------------------------

enabled = False
def comment (obj):
  print '>> ' + str(obj)

def debug (obj):
  if enabled:
    print obj
  pass

for arg in sys.argv:
  if arg in ('debug'):
    enabled = True
