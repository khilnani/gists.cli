#!/usr/bin/env python

import sys, rest, log, util

#-------------------------------------------

def updateCredentials ():
  rest.updateCredentials()
  sys.exit(0)

#-------------------------------------------

def list ():
  rest.getCredentials()
  log.debug ("Command: List.")

  url = "/gists"
  gists = rest.get(url)
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
  rest.getCredentials()
  log.debug ("Command: Create: " + str(public) + ", " + str(filename) + ", " + str(content))

#-------------------------------------------

def update (id):
  rest.getCredentials()
  log.debug ("Command: Update" + id)

#-------------------------------------------

def append (id):
  rest.getCredentials()
  log.debug ("Command: Append" + id)

#-------------------------------------------

def delete (id):
  rest.getCredentials()
  log.debug ("Command: Delete" + id)

#-------------------------------------------

def get_gist(id):
  rest.getCredentials()
  log.debug ("Internal: get_gist: " + id) 

  url = "/gists/" + id
  gist = rest.get(url)
  return gist

#-------------------------------------------

def view (id):
  log.debug ("Command: View: " + id)
  gist = get_gist(id)
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
  gist = get_gist(id)
  print "Downloading Gist %s files to '%s'" % (id, path)

#-------------------------------------------

