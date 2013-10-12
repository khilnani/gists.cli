#!/usr/bin/env python

import sys, actions, log, util

#-------------------------------------------

_supress = False

#-------------------------------------------

def _hasCmd( args ):
  log.debug ("_hasCmd: " + str(args))
  if len(args) > 0:
    cmd = args[0]
    # Shortcut check: is arg a Bool, File, String with spaces/sp char
    if util.parseBool( cmd ) != None:
      return False
    if util.isFileOrDir( cmd ) == True:
      return False
    if str( cmd ).strip().isalnum() == False:
      return False
    # Cmd: is cmd one of the known commands
    if str(cmd).strip().lower() in ("list","l","token", "t", "view", "v", "get", "g", "create", "c", "new", "n", "append", "a", "update", "u", "delete", "del", "d", "backup", "b", "search", "query", "q"):
      log.debug ("_hasCmd: Found")
      return True
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
  elif cmd in ("list","l"):
    actions.list()
  elif cmd in ("token", "t"):
    actions.updateCredentials()
  elif cmd in ("view", "v"):
    actions.view( args[0] )
  elif cmd in ("get", "g"):
    actions.get( args[0], args[1] )
  elif cmd in ("append", "a"):
    actions.append( args[0] )
  elif cmd in ("update", "u"):
    actions.update( args[0] )
  elif cmd in ("delete", "del", "d"):
    actions.delete( args[0] )
  elif cmd in ("backup", "b"):
    pass
  elif cmd in ("search", "query","q"):
    pass
  elif cmd in ("new", "n", "create", "c"):
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
