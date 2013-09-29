#!/usr/bin/env python

import sys, os.path, rest, log, util

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

def main ( ):

  args = sys.argv
  
  print ''

  if len(args) == 1:
    log.comment ("No arguments specified, listing your Gists. Try '%s help' if you need help." % sys.argv[0])
    print ''

  log.debug ("Arguments " + str( args ))

  del args[0] # Delete the filename
  cmd = None

  """---------------------------------------
  default command if no arguments at all
    list
  """
  if len(args) == 0:
    list()
  else:
    """---------------------------------------
    If args > 1, args[0] is the command. We remove it from the list
    args now contains only the  command arguments
    """
    cmd = args[0]
    del args[0] # Delete the command. Arguments remaining are the options for each command
    log.debug ("Potential cmd: " + cmd)
    log.debug ("Adjusted arguments " + str( args ))

    """ ---------------------------------------
    cmd args = 0:
      create
      ID
      token|t
    """
    if len(args) == 0:
      if cmd in ("new", "n", "create", "c"):
        create()  # Create with no args
      elif cmd in ("token", "t"):
        rest.updateCredentials()
        sys.exit(0)
      else:
        view( cmd )  # if there are no args and the cmd doesnt match, assume the cmd is the gist id
    else:
      """ -----------------------------------------
      cmd args = 1+:
         create CONTENT
         create FILE
         create private
         create private CONTENT
         create private FILE
         append ID
         update ID
         delete ID
         ID path
      """
      if cmd in ("new", "n", "create", "c"):
        if len(args) == 1:
          # check if the arg is a Boolean, File or Content
          if util.parseBool(args[0]) != None:
            create( public = util.parseBool(args[0]) )
          elif util.isFile(args[0]) == True:
            create( filename = args[0] )
          else:
            create( content = args[0] )
        elif len(args) > 1: 
          # args could be boolean and File, or Boolean and Content
          create( )
      elif cmd in ("append", "a"):
        append( args[0] )
      elif cmd in ("update", "u"):
        update( args[0] )
      elif cmd in ("delete", "d"):
        delete( args[0] )
      else:
        # No match = get
        get( cmd, args[0] ) # if no match, cmd has the ID, arg[0] has the path

  log.debug ("Done.")
  print ''
#-------------------------------------------

if __name__ == "__main__":
  main ()

#-------------------------------------------
