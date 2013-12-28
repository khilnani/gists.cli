#!/usr/bin/env python

import os, log, sys, defaults, platform

#-------------------------------------------

_cmds = defaults.cmds

#-------------------------------------------

fileName = os.path.basename(sys.argv[0])

#-------------------------------------------

def argv ( ids ):
# print ("util.argv: " + str(ids))
  for i in range(len(sys.argv)):
    if sys.argv[i] in ids:
      del sys.argv[i]
      # print "util.argv True"
      return True
  # print "util.argv False"
  return False

#-------------------------------------------

def isIOS ():
  log.debug ("platform.system: {0} platform.machine: {1}".format(platform.system(), platform.machine()))
  return platform.system() == 'Darwin' and platform.machine().startswith('iP')

#-------------------------------------------

def isMac ():
  log.debug ("platform.system: {0} platform.machine: {1}".format(platform.system(), platform.machine()))
  return platform.system() == 'Darwin' and not platform.machine().startswith('iP')

#-------------------------------------------

def isLinux ():
  log.debug ("platform.system: {0} platform.machine: {1}".format(platform.system(), platform.machine()))
  return platform.system() == 'Linux' or platform.system() == 'Linux2'

#-------------------------------------------

def isWindows():
  log.debug ("platform.system: {0} platform.machine: {1}".format(platform.system(), platform.machine()))
  return platform.system() == 'Windows'

#-------------------------------------------

def readFile (filename):
  log.debug ("readFile: " + str(filename))
  content = None
  if filename != None and os.path.exists(filename):
    try:
      file = open(filename)
      content = file.read()
      file.close()
    except Exception as e:
      log.error ("Unable to read file '{0}'.".format(filename))
  return content

#-------------------------------------------

def readConsole(prompt='Please type/paste content:', required=True, bool=False):
  content = raw_input(prompt)
  if len( content.strip() ) == 0 and required == True:
    content = readConsole (prompt, required, bool)
  if bool:
    if parseBool(content) == None:
      if required == True:
        content = readConsole (prompt, required, bool)
      else:
        content = None
  return content

#-------------------------------------------

def parseBool (obj):
  log.debug ("parseBool: " + str(obj))
  obj_str = str(obj).strip().lower()
  if obj == True or obj == 1:
    return True
  if obj == False or obj == 0:
    return False
  if obj_str in ("true", "yes", "1", "y"):
    return True
  if obj_str in ("false", "no", "0", "n"):
    return False
  return None

#-------------------------------------------

def isGistIdent (id):
  return isGistID(id) or isGistIndex(id)

#-------------------------------------------

def isGistID (id):
  return id.strip().isalnum() == True

#-------------------------------------------

def isGistIndex (id):
  ret = False
  if len(id) > 1 and id[0] in _cmds['#']:
    try:
      i = int(id[1:])
      ret = True
    except:
      ret = False
  return ret

#-------------------------------------------

def isFileOrDir (obj):
  log.debug ("isFileOrDir: " + str(obj))
  obj_str = str(obj)
  if ' ' in obj_str:
    return False
  elif os.path.isfile(obj_str) or os.path.isdir(obj_str):
    return True
  return False

#-------------------------------------------

def isFile (obj):
  log.debug ("isFile: " + str(obj))
  obj_str = str(obj)
  if ' ' in obj_str:
    return False
  elif os.path.isfile(obj_str) and not os.path.islink(obj_str):
    return True
  return False

#-------------------------------------------

def line (msg=""):
  print "------------------------------------------------------------------------------------------" + msg

#-------------------------------------------

if __name__ == '__main__':
  print ''
  print 'parseBool'
  print ''
  print parseBool(1)
  print parseBool(0)
  print parseBool('true')
  print parseBool('false')
  print parseBool('Yes')
  print parseBool('no')
  print parseBool('1')
  print parseBool('what?')
  print parseBool(' ')
  print ''
  print 'isFile'
  print ''
  print isFile('')
  print isFile('My Name is')
  print isFile('/usr')
  print isFile('util.py')
