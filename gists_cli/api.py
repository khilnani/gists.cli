#!/usr/bin/env python

import sys, os.path, json, getpass, requests, log, util


#-------------------------------------------
# Config

GITHUB_API = "https://api.github.com"
HOME_DIR = '~/Documents' if util.isIOS() == True else '~'
HOME = os.path.expanduser(HOME_DIR)
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
    log.error ("Insufficient privilages to write the access token to %s." % (HOME + TOKENFILE))
    log.error ("Message: " + str(e))


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
  elif username == None or password == None:
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
      log.debug ('API (Get): ' + request.url)
    else:
      request = requests.get( url, auth=(username, password), params=params )
      log.debug ('API (Get): ' + request.url)
    _checkStatus( request.status_code )
    result = json.loads( request.text )
  except Exception as e:
    print 'Oops. We had a slight problem with the GitHub SSO: ' + str( e ) 
    sys.exit(0)
  return result  

#-------------------------------------------

def post (path, data={}, params={}):
  global token, username, password
  result = None
  url = GITHUB_API + path
  data = json.dumps(data)
  log.debug ('Json data: ' + data)
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  try:
    if token != None:
      params['access_token'] = token
      request = requests.post( url, params=params, data=data, headers=headers )
      log.debug ('API (Post): ' + request.url)
    else:
      request = requests.post( url, auth=(username, password), params=params, data=data, headers=headers )
      log.debug ('API (Post): ' + request.url)
    _checkStatus( request.status_code )
    result = json.loads( request.text )
  except Exception as e: 
    print 'Oops. We had a slight problem with the GitHub SSO: ' + str( e )
    sys.exit(0)
  return result

#-------------------------------------------

def patch (path, data={}, params={}):
  global token, username, password
  result = None
  url = GITHUB_API + path
  data = json.dumps(data)
  log.debug ('Json data: ' + data)
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  try:
    if token != None:
      params['access_token'] = token
      request = requests.patch( url, params=params, data=data, headers=headers )
      log.debug ('API (Patch): ' + request.url)
    else:
      request = requests.patch( url, auth=(username, password), params=params, data=data, headers=headers )
      log.debug ('API (Patch): ' + request.url)
    _checkStatus( request.status_code )
    result = json.loads( request.text )
  except Exception as e: 
    print 'Oops. We had a slight problem with the GitHub SSO: ' + str( e )
    sys.exit(0)
  return result

#-------------------------------------------

def _checkStatus (code):
  log.debug ('Github API Response Code: %s' % str(code))
  if code == 200 or code == 201 or code == 204:
    pass
  elif code == 404 or code == 403:
    print 'Please check your user name and/or password.'
    sys.exit(0)
  elif code == 400:
    print 'Bad Request'
    sys.exit(0)
  elif code == 422:
    print 'Unprocessable Entity'
    sys.exit(0)
  else:
    print 'Uknown Error: ' + str(code)
    sys.exit(0)

