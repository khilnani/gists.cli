#!/usr/bin/env python

import sys, urllib2, base64, json, getpass

#-------------------------------------------

GITHUB_API = "https://api.github.com"

#-------------------------------------------

def debug (obj):
  print obj

#-------------------------------------------

def auth ():
  result=''
  username = raw_input("Username:")
  password = getpass.getpass()
  try:
    request = urllib2.Request( GITHUB_API + "/user" )
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string) 
    response = urllib2.urlopen(request) 
#    debug( response.info() )
    result = response.read()
    response.close()
  except urllib2.HTTPError as httpe:
    print 'Github Authentication error: %s' % str(httpe)
    print 'Please check your user name and/or password.'
    sys.exit(0)
  except Exception as e:
    print 'Oops. We had a slight problem with the GitHub SSO: ' + str( e )
    sys.exit(0)
#  debug( result )
  json_obj = json.loads( result )
  public_gists = json_obj['public_gists']
  private_gists = json_obj['private_gists']
  print 'You have %i Private Gists and %i Public Gists' % (private_gists, public_gists)
  return result


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
