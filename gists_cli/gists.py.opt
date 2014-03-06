#!/usr/bin/env python

import sys, actions, log, util
from optparse import OptionParser
from optparse import OptionGroup
#-------------------------------------------

_supress = False

parser = OptionParser("\n\r\n\r    Manage your Gists!")
parser.add_option("--list","-l", action="store_const", const="list", dest="cmd", help="List your public and private Gists.")
parser.add_option("--token","-t", action="store_const", const="token", dest="cmd", help="Set your GitHub OAuth token to avoid the username/password prompt.")
parser.add_option("--view","-v", action="store_const", const="view", dest="cmd", help="View a Gist's content on screen.")
parser.add_option("--get","-g", action="store_const", const="get", dest="cmd", help="Download a Gist.")
parser.add_option("--create","-c","--new","-n", action="store_const", const="create", dest="cmd", help="Create a new Gist.")
parser.add_option("--supress", "-s", action="store_true", dest="supress", default=False, help="Supress all prompts, assume default response 'yes'.")

group = OptionGroup(parser, "Incomplete Options","The following options have not been implemented.")

group.add_option("--append","-a", action="store_const", const="append", dest="cmd", help="Append text to an existing Gist.")
group.add_option("--update","-u", action="store_const", const="update", dest="cmd", help="Update (replace) a Gist.")
group.add_option("--delete","--del","-d", action="store_const", const="delete", dest="cmd", help="Delete a Gist.")
group.add_option("--search","--query","-q", action="store_const", const="search", dest="cmd", help="Search your Gists - descriptions and text file content.")
group.add_option("--export","-e","--backup","-b", action="store_const", const="export", dest="cmd", help="Export or Backup all of your Gists.")

parser.add_option_group(group)

(options, args) = parser.parse_args()

#-------------------------------------------

def _hasCmd( _args ):
  global options, args
  log.debug ("_hasCmd: " + str(args))
  log.debug ("_hasCmd: " + str(options.cmd))
  if options.cmd:
    return True
  log.debug ("_hasCmd: No Command Found") 
  return False

#-------------------------------------------

def _deriveCmd( args ):
  log.debug ("_deriveCmd: " + str(args))
  cmd = None
  alen = len(args)

  if alen == 0:
    # list
    cmd = "list"
  elif alen == 1:
    if args[0].strip().isalnum() == True and util.isFileOrDir( args[0] ) == False  and util.parseBool( args[0] ) == None:
      # view ID
      cmd = "view"
    elif util.isFileOrDir( args[0] ) == True:
      # create FILE 
      cmd = "create"
    elif args[0].strip().isalnum() == False:
      # create 'Content'
      cmd = "create"
  elif alen == 2:
    if str(args[0]).strip().isalnum() and util.parseBool( args[0] ) == None:
      # get ID 'Dir'
      cmd =  "get"
    else:
      # create Boolean and File
      # create Boolean and Content
      # create Description and File
      # create Description and Content
      cmd = "create"
  elif alen == 3 and util.parseBool( args[0] ) != None:
      # create Boolean, Description and File
      # create Boolean, Description and Content
      cmd = "create"
  return cmd

#-------------------------------------------

def _printNoMatch():
  print 'Unfortunately, no command match found for supplied arguments.'

#-------------------------------------------

def main ( ):

  global _supress

  print ''

  log.setDebug( util.argv(["debug"]) )
  actions.supress( util.argv(["s", "silent","supress"]) )

  args = sys.argv
  
  if len(args) == 1:
    log.comment ("No arguments specified, listing your Gists. Try '%s help' if you need help." % sys.argv[0])
    print ''

  del args[0] # Delete the filename
  cmd = None

  log.debug ("Arguments " + str( args ))

  #--------------------------------------------
  # If args[0] is a command. We remove it from the list. args now contains only the  command arguments
  # else we keep as is and try to evaluate the command
  #--------------------------------------------
  if _hasCmd( args ):
    cmd = args[0]
    del args[0] # Delete the command. Arguments remaining are the options for each command
  else:
    cmd = _deriveCmd( args )

  log.debug ("Adjusted cmd: " + str(cmd))
  log.debug ("Adjusted arguments " + str( args ))
  #--------------------------------------------
  # Handle commands
  #--------------------------------------------
  if cmd == None:
    _printNoMatch()
  elif cmd in ("list","--list","l","-l"):
    actions.list()
  elif cmd in ("token","--token","t","-t"):
    actions.updateCredentials()
  elif cmd in ("view","--view","v","-v"):
    actions.view( args[0] )
  elif cmd in ("get","--get","g""-g"):
    actions.get( args[0], args[1] )
  elif cmd in ("append","--append","a","-a"):
    actions.append( args[0] )
  elif cmd in ("update","--update","u","-u"):
    actions.update( args[0] )
  elif cmd in ("delete","--delete","del","--del","d","-d"):
    actions.delete( args[0] )
  elif cmd in ("backup","--backup","b","-b"):
    pass
  elif cmd in ("search","--search","query","--query","q","-q"):
    pass
  elif cmd in ("new","--new","n","-n", "create","--create","c","-c"):
    # Each option will prompt for public/pvt and description. In silent mode, assumes private and no description.
    if len(args) == 0:
      actions.create()
    elif len(args) == 1:
      # create File
      # create Content
      if util.isFileOrDir(args[0]) == True:
        actions.create( filename = args[0] )
      else:
        actions.create( content = args[0] )
    elif len(args) == 2: 
      # create Boolean and File
      # create Boolean and Content
      # create Description and File 
      # create Description and Content 
      if util.parseBool( args[0] ) != None:
        if util.isFileOrDir(args[1]) == True:
          actions.create( public=util.parseBool( args[0] ), filename=args[1] )
        else:
          actions.create( public=util.parseBool( args[0] ), content=args[1] )
      else:
        if util.isFileOrDir(args[1]) == True:
          actions.create( description=args[0], filename=args[1] )
        else:
          actions.create( description=args[0], content=args[1] )
    elif len(args) == 3 and util.parseBool( args[0] ) != None:
      # create Boolean, Description and File
      # create Boolean, Description and Content
      if util.isFileOrDir(args[2]) == True:
        actions.create( public=util.parseBool( args[0] ), description=args[1], filename=args[2] )
      else:
        actions.create( public=util.parseBool( args[0] ), description=args[1], content=args[2] )
    else:
      _printNoMatch()
  else:
    _printNoMatch()

  log.debug ("Done.")
  print ''

#-------------------------------------------

if __name__ == "__main__":
  main ()

#-------------------------------------------
