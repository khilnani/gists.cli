#!/usr/bin/env python

# http://docs.python-requests.org/en/latest/user/quickstart/
# http://www.pythonforbeginners.com/
# http://docs.python.org/2/tutorial/inputoutput.html

import sys, os.path, rest, log

#-------------------------------------------

def list ():
  rest.getCredentials()
  log.debug ("List.")

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
    print '{0:4} {1:30} {2:8} {3:25} {4}'.format(i, file_list, str(gist['public']), gist['id'], gist['description'])
  print "You have %i Gists. (%i Private)" % (len(gists), private_count)

#-------------------------------------------

def create ():
  rest.getCredentials()
  log.debug ("Create.")

#-------------------------------------------

def update (id):
  rest.getCredentials()
  log.debug ("Update" + id)

#-------------------------------------------

def append (id):
  rest.getCredentials()
  log.debug ("Append" + id)

#-------------------------------------------

def delete (id):
  rest.getCredentials()
  log.debug ("Delete" + id)

#-------------------------------------------

def get_gist(id):
  rest.getCredentials()
  log.debug ("get_gist: " + id) 

  url = "/gists/" + id
  gist = rest.get(url)
  return gist

#-------------------------------------------

def view (id):
  log.debug ("View: " + id)
  gist = get_gist(id)
  for (file, data) in gist['files'].items():
    content = data['content']
    print 'Gist: {:25} File: {}'.format(id, file)
    print '-------------------------------------------------------------------START'
    print content
    print '-------------------------------------------------------------------END'

#-------------------------------------------

def get (id, path):
  log.debug ("Get: %s, %s" % (id, path))
  gist = get_gist(id)
  print "Downloading Gist %s files to '%s'" % (id, path)

#-------------------------------------------

def main ( args ):

  print ''
  log.debug ("Arguments " + str( args ))

  del args[0] # Delete the filename
  cmd = None

  """---------------------------------------
  args = 0: 
    list
  """
  if len(args) == 0:
    list()
  else:
    cmd = args[0]
    arg_len = len(args)
    del args[0] # Delete the command. Arguments remaining are the options for each command
    log.debug ("Potential cmd: " + cmd)
    log.debug ("Adjusted arguments " + str( args ))

    """ ---------------------------------------
    args = 1:
      create, ID, token 
    """
    if arg_len == 1:
      if cmd in ("new", "n", "create", "c"):
        create()
      elif cmd in ("token", "t"):
        rest.updateCredentials()
        sys.exit(0)
      else:
        view( cmd )  # if there is only 1 arg and its not a command, its the gist id
    else:
      """ -----------------------------------------
      args = 2+:
         append ID
         update ID
         delete ID
         ID path
      """
      if cmd in ("append", "a"):
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
  if len(sys.argv) == 1:
    log.comment ("No arguments specified, listing your Gists. Try '%s help' if you need help" % sys.argv[0])
  main (sys.argv)

#-------------------------------------------
