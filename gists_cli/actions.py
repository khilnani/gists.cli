#!/usr/bin/env python

import sys, api, log, util, os, defaults, textwrap
from texttable import Texttable

#-------------------------------------------

_cmds = defaults.cmds
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

def _get_id_for_index(id):
  log.debug("_get_id_for_index: " + str(id))

  _id = ''
  if id[0] in _cmds['#']:
    index = -1
    try:
      index = int(id[1:])
    except ValueError:
      log.error('Please use a valid number as the index.')
      return _id

    log.debug("Using index: " + str(index))
    api.getCredentials()
    url = "/gists"
    gists = api.get(url)
    for (i, gist) in enumerate(gists):
      log.debug("Checking...  gist {0} at index: {1} == {2} ?".format(gist['id'], (i+1), index)) 
      if i+1 == index:
        _id = gist['id']
        log.debug("Found Gist: {0} at index: {1}".format(_id, index))
        break
  return _id

#-------------------------------------------

def list ():
  api.getCredentials()
  log.debug ("Command: List.")

  url = "/gists"
  gists = api.get(url)
  public_count = 0
  private_count = 0

  table = Texttable(max_width=defaults.max_width)
  table.set_deco(Texttable.HEADER | Texttable.HLINES)
  table.set_cols_align(["l", "l", "l", "l", "l"])
  table.set_cols_width([4, 30, 6, 20, 30])

  table.header( ["","Files","Public", "Gist ID",  "Description"] )

  for (i, gist) in enumerate(gists):
    private = False
    file_list = ''
    for (file, data) in gist['files'].items():
      file_list += "'" + file + "' " 
    if gist['public']:
      public_count += 1
    else:
      private_count += 1
    table.add_row( [i+1, file_list, str(gist['public']), gist['id'], gist['description']] )

  print table.draw()

  print ''
  print "You have %i Gists. (%i Private)" % (len(gists), private_count)

#-------------------------------------------

def new (public=None,description=None,content=None,filename=None):
  api.getCredentials()
  log.debug ("Command: New: public: '{0}' description: '{1}' filename: '{2}' content: '{3}'.".format(str(public), str(description), str(filename), str(content)))

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
      print "Sorry, filename '{0}' is actually a Directory.".format(filename)
      sys.exit(0)

  if content == None:
    if _supress:
      content = defaults.content
    else:
      content = util.readConsole()

  if filename == None:
    filename = defaults.file

  log.debug ("Creating Gist using content: \n" + content)

  url = '/gists'
  data = {'public': str(public).lower(), 'description': description, 'files': { os.path.basename(filename): { 'content': content } } }
  log.debug ('Data: ' + str(data))

  gist = api.post(url, data=data)

  pub_str = 'Public' if gist['public'] else 'Private'
  print "{0} Gist created:Id '{1}' and Url: {2}".format(pub_str, gist['id'], gist['html_url'])


#-------------------------------------------

def _get_gist(id):
  api.getCredentials()
  log.debug ("Internal: _get_gist: " + id) 

  url = "/gists/" + id
  gist = api.get(url)
  return gist

#-------------------------------------------

def view (id, fileName=''): 
  log.debug("Viewing Gist with ID: {0} and fileName: '{1}'".format(id,fileName))

  if id[0] in _cmds['#']:
    id = _get_id_for_index(id)

  if id:
    gist = _get_gist(id)
    # display line delims only if more than one file exists. facilitates piping file content
    noDelim = len(gist['files']) == 1 or fileName != ''
    for (file, data) in gist['files'].items():
      content = data['content']
      if not noDelim:
        util.line()
        print 'Gist: {0} File: {1}'.format(id, file)
        util.line()
      if fileName != '':
        if fileName.strip().lower() == file.strip().lower():
          print content
      else:
        print content
      if not noDelim:
        util.line()

#-------------------------------------------

def get (id, path, fileName=''):
  log.debug ("Downloading Gist with Id '{0}' (fileName: {1}) to '{2}'.".format (id, fileName, path))

  if id[0] in _cmds['#']:
    id = _get_id_for_index(id)

  if id:
    gist = _get_gist(id)
    target = os.path.join(path,id)

    print ('Gist \'{0}\' has {1} file(s)'.format(id, len(gist['files'])))
    for file in gist['files']:
      print ('  ' + file)
    dmsg = 'file(s)' if fileName == '' else "'" + fileName + "'"
    confirm = util.readConsole(prompt="Download {0} to (1) '{1}/' or (2) '{2}/'?: ".format(dmsg, path, target))
    if confirm in ('1', '2'):
      filesDownloaded = 0
      try:
        if not os.path.isdir(path):
          os.makedirs(path)
        if confirm == '1':
          target = path
        else:
          os.makedirs(target)
        for (file, data) in gist['files'].items():
          downLoadFile = False
          if fileName != '':
            if fileName.strip().lower() == file.strip().lower():
              downLoadFile = True
          else:
            downLoadFile = True
          if downLoadFile == True:
            content = data['content']
            filepath = os.path.join(target,file)
            file = open( filepath , 'w')
            file.write(content)
            file.close()
            filesDownloaded += 1
            log.debug( 'Saved file:' + filepath )
        print ('{0} File(s) downloaded.'.format(filesDownloaded))
      except Exception as e:
        print "Insufficient privilages to write to %s." % target
        print "Error message: " + str(e)
    else:
      print 'Ok. I won\'t download the Gist.'


#-------------------------------------------

def append (id, description=None,content=None,filename=None):
  api.getCredentials()
  log.debug ("Command: Append: id: '{0}' description: '{1}' filename: '{2}' content: '{3}'.".format(id, str(description), str(filename), str(content)))

  if id[0] in _cmds['#']:
    id = _get_id_for_index(id)

  if description == None:
    if _supress:
      description = defaults.description
    else:
      description = util.readConsole(prompt='Description:', required=False)

  if content == None and filename != None:
    if os.path.isfile( filename ):
      content = util.readFile(filename)
    else:
      print "Sorry, filename '{0}' is actually a Directory.".format(filename)
      sys.exit(0)

  if content == None:
    if _supress:
      content = defaults.content
    else:
      content = util.readConsole(required=False)

  if filename == None:
    filename = defaults.file

  log.debug ("Appending Gist " + id + " with content: \n" + content)
  
  oldgist = _get_gist(id)
  
  if description and description != '?':
    oldgist['description'] = description
  if content and content != '?':
    for (file, data) in oldgist['files'].items():
      oldgist['files'][file]['content'] = data['content'] + '\n' + content
  log.debug ('Data: ' + str(oldgist))

  url = '/gists/' + id
  gist = api.patch(url, data=oldgist)

  pub_str = 'Public' if gist['public'] else 'Private'
  print "{0} Gist appended: Id '{1}' and Url: {2}".format(pub_str, gist['id'], gist['html_url'])


#-------------------------------------------

def update (id, description=None,content=None,filename=None):
  api.getCredentials()
  log.debug ("Command: Update: id: '{0}' description: '{1}' filename: '{2}' content: '{3}'.".format(id, str(description), str(filename), str(content)))

  if id[0] in _cmds['#']:
    id = _get_id_for_index(id)

  if description == None:
    if _supress:
      description = defaults.description
    else:
      description = util.readConsole(prompt='Description:', required=False)

  if content == None and filename != None:
    if os.path.isfile( filename ):
      content = util.readFile(filename)
    else:
      print "Sorry, filename '{0}' is actually a Directory.".format(filename)
      sys.exit(0)

  if content == None:
    if _supress:
      content = defaults.content
    else:
      content = util.readConsole(required=False)

  if filename == None:
    filename = defaults.file

  log.debug ("Updating Gist " + id + " with content: \n" + content)

  url = '/gists/' + id
  data = {}
  if description and description != '?':
    data['description'] = description
  if content and content != '?':
    data['files'] = { os.path.basename(filename): { 'content': content } }
  log.debug ('Data: ' + str(data))

  gist = api.patch(url, data=data)

  pub_str = 'Public' if gist['public'] else 'Private'
  print "{0} Gist updated: Id '{1}' and Url: {2}".format(pub_str, gist['id'], gist['html_url'])

#-------------------------------------------

def delete (id):
  api.getCredentials()
  log.debug ("Command: Delete: " + id)

  if id[0] in _cmds['#']:
    id = _get_id_for_index(id)

  confirm = defaults.forceDelete
  
  if _supress == False:
    gist = _get_gist(id)

    print ('Gist \'{0}\'  Description: {1}'.format(id, gist['description']))
    for file in gist['files']:
      print ('  ' + file)
    confirm = util.parseBool( util.readConsole(prompt='Delete Gist? (y/n):', required=False, bool=True) )

  if confirm:
    url = '/gists/' + id
    api.delete(url)
    print 'Gist deleted: {0}'.format(id)
  else:
    print 'I did not delete the Gist.'

#-------------------------------------------

def backup ():
  api.getCredentials()
  log.debug ("Command: Backup.")

#-------------------------------------------

def search ():
  api.getCredentials()
  log.debug ("Command: Search.")

#-------------------------------------------

def _getHelpTableRow (action, args='', help=''):
  l = []
  l.append(action)
  l.append(util.fileName + ' ' + '|'.join(_cmds[action]) + ' ' + args)
  l.append(help)
  return l
  
#-------------------------------------------

def help ():
  log.debug ("Help command.")

  print 'Gists.CLI'
  print ''
  print textwrap.fill('An easy to use CLI to manage your GitHub Gists. Create, edit, append, view, search and backup your Gists.', defaults.max_width)
  print ''
  print 'Author: Nik Khilnani - https://github.com/khilnani/gists.cli'
  print ''
  print "Note - GIST_ID can be a Gist ID or Index ID (of the Gist in the List view)."
  print "Index is 1 based and must be in the format '#N', '%N' , '.N' or ':N'."

  table = Texttable(max_width=defaults.max_width)
  table.set_deco(Texttable.HEADER | Texttable.HLINES)
  table.set_cols_align(["l", "l", "l"])
  table.set_cols_width([8, 45, 37])

  table.header( ["Action","Usage", "Description"] )
  
  table.add_row( _getHelpTableRow("Help", help='Display the help documentation') )

  table.add_row( _getHelpTableRow("Token", 'TOKEN', help='Save your Github  OAuth Token. Will be prefeered over ~/.git-credentials to avoid user/password prompts. Saves to ~/.gists') )

  table.add_row( _getHelpTableRow("List", help='Lists your public and private Gists.') )

  table.add_row( _getHelpTableRow("View", "GIST_ID|'.'INDEX [FILE]", help="Displays contents of a Gist on screen. To view a specific file, specify [FILE]. Instead of the Gist ID, the (1 based) index of the Gist in the List screen can be used. eg. %1, .1, :1 or '#1'") )

  table.add_row( _getHelpTableRow("Download", "GIST_ID|'.'INDEX PATH [FILE]", help="Get or Download the files in a Gist to (1) Current Directory, or (2) Directory with Gist ID as its name. To download a specific file, specify [FILE]. Instead of the Gist ID, the (1 based) index of the Gist in the List screen can be used. eg. %1, .1, :1 or '#1'") )

  table.add_row( _getHelpTableRow("New", '[PUBLIC_BOOL] [DESCRIPTION] [CONTENT|FILE]', help='Create a new Gist. Will prompt for Public/Private, Description etc. if not provided as arguments. Default is Private.') )

  table.add_row( _getHelpTableRow("Append", 'GIST_ID [DESCRIPTION] CONTENT|FILE', help="Will append to each file in a Gist. Use '?' to keep current value.") )

  table.add_row( _getHelpTableRow("Update", 'GIST_ID [DESCRIPTION] CONTENT|FILE', help="Update the content of a Gist if a file name match is found. If not, a new file is added. Use '?' to keep current value.") )

  table.add_row( _getHelpTableRow("Delete", help='Delete a Gist.') )

  table.add_row( _getHelpTableRow("Backup", help='Backup or Export all Gists. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Search", help='Text search the content of your Gists. NOT IMPLEMENTED') )

  table.add_row( _getHelpTableRow("Supress", help='Supress prompts. Defaults will be used.') )

  table.add_row( _getHelpTableRow("Debug", help='Output Debug info. NOTE - Reveals sesnitive info such as OAuth tokens.') )

  print table.draw()

#-------------------------------------------

