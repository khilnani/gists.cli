#!/usr/bin/env python

import sys, os.path, json, getpass, requests, log


#-------------------------------------------
# Config

GITHUB_API = "https://api.github.com"
HOME = os.path.expanduser('~')
TOKENFILE = '/.gist'

#-------------------------------------------
# Globals

token = None
username = None
password = None

#-------------------------------------------

def getCredentials (): 
  global token, username, password
  if( os.path.exists( HOME + TOKENFILE) ):
    file = open(HOME + TOKENFILE, 'r')
    token = file.read().strip()
    log.debug ('Token from file: ' + token)
  else:
    log.debug (HOME + TOKENFILE + ' not found.')
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
      log.debug (request.url)
    else:
      request = requests.get( url, auth=(username, password), params=params )
      log.debug (request.url)
    if request.status_code != 200:
      print 'Github Authentication error: %s' % str(request.status_code)
      print 'Please check your user name and/or password.'
      sys.exit(0)
    result = json.loads( request.text )
  except Exception as e:
    print 'Oops. We had a slight problem with the GitHub SSO: ' + str( e ) 
    sys.exit(0)
  return result  
