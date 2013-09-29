#!/usr/bin/env python

import os, sys

version = '0.2'
target_path = os.path.expanduser('~') + '/bin' if len(sys.argv) == 1 else sys.argv[1]

print ''
confirm = raw_input('Install Gist (' + version + ') to \'' + target_path + '\' ? (y/n):')
if confirm == 'y':
  pass
else:
  print 'USAGE: ./install.py INSTALL_PATH'
  print ''
  sys.exit(0)

target_dir = '{0}/gist-{1}'.format(target_path, version)

if not os.path.exists(target_path):
  print ('{} not found. Creating.'.format(target_path))
  os.system ('mkdir ' + target_path)

if os.path.exists(target_path):
  if os.path.exists(target_dir):
    print ('Removing old ' + target_dir)
    os.system('rm -rf ' + target_dir)
  print ('Copying files to {0}'.format(target_dir))
  os.system ('cp -rf ./src {0}'.format(target_dir))
  print ('Creating {0}/gist alias'.format(target_path))
  os.system ('ln -sf {0}/gist.py {1}/gist'.format(target_dir,target_path))
  print ('Done.')
  print ('Please make sure you add \'{0}\' to your $PATH. Type \'gist\' to execute.'.format(target_path))
else:
  print ('Unable to copy. {0} could not be created or does not exist. Sorry.'.format(target_path))
print ''
