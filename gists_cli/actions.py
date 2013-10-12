#!/usr/bin/env python

import sys, api, log, util, os, defaults

#-------------------------------------------

_supress = False

#-------------------------------------------

def supress( s ):
  global _supress
  _supress = s
  log.debug ("_supress: " + str(_supress))


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

def create (public=None,description=None,content=None,filename=None):
  api.getCredentials()
  log.debug ("Command: Create: public: '{}' description: '{}' filename: '{}' content: '{}'.".format(str(public), str(description), str(filename), str(content)))

  if public == None:
    if _supress:
      public = defaults.public
    else:
      public = util.parseBool( util.readConsole(prompt='Public Gist? (y/n):', bool=True) )

  if description == None:
    if _supress:
      description = defaults.description
    else:
      description = util.readConsole(prompt='Description:', required=False)

  if content == None and filename != None:
    if os.path.isfile( filename ):
      content = util.readFile(filename)
    else:
      print "Sorry, filename '{}' is actually a Directory.".format(filename)
      sys.exit(0)

  if content == None:
    if _supress:
      content = defaults.content
    else:
      content = util.readConsole()

  if filename == None:
    filename = 'file.md'

  log.debug ("Creating Gist using content: \n" + content)

  url = '/gists'
  data = {'public': str(public).lower(), 'description': description, 'files': { os.path.basename(filename): { 'content': content } } }
  log.debug ('Data: ' + str(data))

  gist = api.post(url, data=data)

  pub_str = 'Public' if gist['public'] else 'Private'
  print "{} Gist created with Id '{}' and Url: {}".format(pub_str, gist['id'], gist['html_url'])


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
  print ("Fetching Gist with Id '%s'." % id)
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
  log.debug ("Downloading Gist with Id '%s' to '%s'." % (id, path))

  gist = _get_gist(id)
  target = os.path.join(path,id)

  print ('Gist \'{}\' has {} file(s)'.format(id, len(gist['files'])))
  for file in gist['files']:
    print ('  ' + file)
  confirm = raw_input ("Download to '{}'? (y/n): ".format(target))
  if confirm == 'y':
    try:
      if not os.path.isdir(path):
        os.makedirs(path)
      os.makedirs(target)
      for (file, data) in gist['files'].items():
        content = data['content']
        filepath = os.path.join(target,file)
        file = open( filepath , 'w')
        file.write(content)
        file.close()
        log.debug( 'Wrote file:' + filepath )
      print 'Download complete.'
    except Exception as e:
      print "Insufficient privilages to write to %s." % target
      print "Error message: " + str(e)
  else:
    print 'Ok. I won\'t download the Gist.'


#-------------------------------------------

