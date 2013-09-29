#!/usr/bin/env python

import os

def parseBool( obj ):
  obj_str = str(obj).strip().lower()
  if obj == True or obj == 1:
    return True
  if obj == False or obj == 0:
    return False
  if obj_str in ("true", "yes", "1"):
    return True
  if obj_str in ("false", "no", "0"):
    return False
  return None

def isFile( obj ):
  obj_str = str(obj)
  if ' ' in obj_str:
    return False
  elif os.path.isfile(obj_str) and not os.path.islink(obj_str):
    return True
  return False

def line(msg=""):
  print "---------------------------------------------------------------------------------------------" + msg

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
