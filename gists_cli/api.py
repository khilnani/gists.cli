#!/usr/bin/env python

import sys, os.path, json, getpass, requests, log


#-------------------------------------------
# Config

GITHUB_API = "https://api.github.com"
HOME = os.path.expanduser('~')
TOKENFILE = '/.gists'                # first line with TOKEN. Checked first.
CREDENTIALS = '/.git-credentials'   # Uses first entry. Format: https://USER:TOKEN@github.com Checked second. 

#-------------------------------------------
# Globals

token = None
username = None
password = None

#-------------------------------------------

def updateCredentials ():
  global token
  new_token = getpass.getpass("Enter/Paste the new GitHub OAuth token:")
  try:
    file = open(HOME + TOKENFILE, "w")
    file.write( new_token )
    file.close()
    token = new_token
    print "New token written to: " + HOME + TOKENFILE
  except Exception as e:
    print "Insufficient privilages to write the access token to %s." % (HOME + TOKENFILE)
    print "Error message: " + str(e)


def getCredentials (): 
  global token, username, password
  if os.path.exists( HOME + TOKENFILE):
    file = open(HOME + TOKENFILE, 'r')
    token = file.read().strip()
    log.debug ("Credentials: " + HOME + TOKENFILE + " = " + token)
  elif os.path.exists( HOME + CREDENTIALS):
    file = open(HOME + CREDENTIALS, 'r')
    line = file.read().strip()
    token = line.split(':')[2].split('@')[0]
    log.debug ("Credentials: " + HOME + CREDENTIALS + " = " + token)
  else:
    log.debug ("Credentials: No token found.")
    username = raw_input("Username:")
    password = getpass.getpass()

#-------------------------------------------

def get (path, params={}):
  global token, username, password
  result = None
  url = GITHUB_API + path
  try:
    if token != None:
      params['access_token'] = token
      request = requests.get( url, params=params )
      log.debug ('API: ' + request.url)
    else:
      request = requests.get( url, auth=(username, password), params=params )
      log.debug ('API: ' + request.url)
    if request.status_code != 200:
      print 'Github API Error: %s' % str(request.status_code)
      print 'Please check your user name and/or password.'
      sys.exit(0)
    result = json.loads( request.text )
  except Exception as e:
    print 'Oops. We had a slight problem with the GitHub SSO: ' + str( e ) 
    sys.exit(0)
  return result  
