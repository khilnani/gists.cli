#!/usr/bin/env python

import os

target = os.path.expanduser('~') + '/bin'

if not os.path.exists(target):
  print ('%s not found. Creating.' % target)
  os.system ('mkdir ' + target)

if os.path.exists(target):
  print ('Copying files to %s' % target)
  os.system ('cp -f src/* %s' % target)
  print ('Done.')
else:
  print ('Unable to copy. %s could not be created and does not exist' % target)
