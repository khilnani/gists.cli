#!/usr/bin/env python

from __future__ import print_function
import os, sys

package = 'gists_cli'
alias = 'gists'
version = '0.351'
target_path = '/usr/local/bin' if len(sys.argv) == 1 else sys.argv[1]

print('')
confirm = raw_input('Install ' + package +' (' + version + ') to \'' + target_path + '\' ? (y/n):')
if confirm == 'y':
  pass
else:
  print('USAGE: ./install.py INSTALL_PATH')
  print('')
  sys.exit(0)

target_dir = '{0}/{1}-{2}'.format(target_path, package, version)

if not os.path.exists(target_path):
  print ('{} not found. Creating.'.format(target_path))
  os.system ('mkdir ' + target_path)

if os.path.exists(target_path):
  if os.path.exists(target_dir):
    print ('Removing old ' + target_dir)
    os.system('rm -rf ' + target_dir)
  print ('Copying files to {0}'.format(target_dir))
  os.system ('cp -rf ./{0} {1}'.format(package, target_dir))
  print ('Creating {0}/{1} alias'.format(target_path, alias))
  os.system ('ln -sf {0}/{2}.py {1}/{2}'.format(target_dir,target_path, alias))
  print ('Done.')
  print ('Please make sure you add \'{0}\' to your $PATH. Type \'{1}\' to execute.'.format(target_path, alias))
else:
  print ('Unable to copy. {0} could not be created or does not exist. Sorry.'.format(target_path))
print('')
