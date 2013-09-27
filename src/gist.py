#!/usr/bin/env python

import sys, os, subprocess, getopt

#-------------------------------------------

def curl(command):
  result=''
  try:
    result = subprocess.call(command, shell=False)
  except:
    print 'Error authenticating against github'
    sys.exit(0)
  return result

def auth ():
  user = raw_input("Username:")
  op = curl( ['curl', '-u', user, 'https://api.github.com/user'] )
  print "--"
  print op

#-------------------------------------------

def list ():
  print "List"

#-------------------------------------------

def add ():
  print "Add"

#-------------------------------------------

def update ():
  print "Update"

#-------------------------------------------

def delete ():
  print "Delete"

#-------------------------------------------

def get ():
  print "Get"

#-------------------------------------------

def main ( args ):
  print "Main " + str( args )

  auth()

  cmd = args[1]

  if cmd in ("list", "l"):
    list()

  if cmd in ("add", "a"):
    add()

  if cmd in ("update", "u"):
    update()

  if cmd in ("delete", "d"):
    delete()

  if cmd in ("get", "g"):
    get()
    
  print "Done."

#-------------------------------------------

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print "No arguments specified. Try %s help " % sys.argv[0]
  else:
    main (sys.argv)

#-------------------------------------------
