#!/usr/bin/env python

import sys, api, log, util

#-------------------------------------------

def updateCredentials ():
  api.updateCredentials()
  sys.exit(0)

#-------------------------------------------

def list ():
  api.getCredentials()
  log.debug ("Command: List.")

  url = "/gists"
  gists = api.get(url)
  public_count = 0
  private_count = 0
  print '{0:4} {1:30} {2:8} {3:25} {4}'.format('', 'Files', 'Public', 'Id', 'Description')
  print '{0:4} {1:30} {2:8} {3:25} {4}'.format('', '-----', '------', '--', '-----------')
  for (i, gist) in enumerate(gists):
    private = False
    file_list = ''
    for (file, data) in gist['files'].items():
      file_list += file 
    if gist['public']:
      public_count += 1
    else:
      private_count += 1
    print '{0:4} {1:30} {2:8} {3:25} {4}'.format(i+1, file_list, str(gist['public']), gist['id'], gist['description'])
  print ''
  print "     You have %i Gists. (%i Private)" % (len(gists), private_count)

#-------------------------------------------

def create (public=False,content=None,filename=None):
  api.getCredentials()
  log.debug ("Command: Create: " + str(public) + ", " + str(filename) + ", " + str(content))

#-------------------------------------------

def update (id):
  api.getCredentials()
  log.debug ("Command: Update" + id)

#-------------------------------------------

def append (id):
  api.getCredentials()
  log.debug ("Command: Append" + id)

#-------------------------------------------

def delete (id):
  api.getCredentials()
  log.debug ("Command: Delete" + id)

#-------------------------------------------

def _get_gist(id):
  api.getCredentials()
  log.debug ("Internal: _get_gist: " + id) 

  url = "/gists/" + id
  gist = api.get(url)
  return gist

#-------------------------------------------

def view (id):
  log.debug ("Command: View: " + id)
  gist = _get_gist(id)
  for (file, data) in gist['files'].items():
    content = data['content']
    util.line()
    print 'Gist: {:25} File: {}'.format(id, file)
    util.line('START')
    print content
    util.line('END')

#-------------------------------------------

def get (id, path):
  log.debug ("Get: %s, %s" % (id, path))
  gist = _get_gist(id)
  print "Downloading Gist %s files to '%s'" % (id, path)

#-------------------------------------------

