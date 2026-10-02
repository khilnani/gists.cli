#!/usr/bin/env python

from __future__ import print_function, absolute_import
import sys, os.path, json, getpass, requests
from . import log, util

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
authcode = None

#-------------------------------------------

def updateCredentials ():
  global token
  new_token = getpass.getpass("Enter/Paste the new GitHub OAuth token:")
  try:
    file = open(HOME + TOKENFILE, "w")
    file.write( new_token )
    file.close()
    token = new_token
    print("New token written to: " + HOME + TOKENFILE)
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
    username = input("Username: ")
    password = getpass.getpass()
    token = None
    auth(username, password)

#-------------------------------------------

def get (path, params={}):
  return call('get', path, params=params)

#-------------------------------------------

def post (path, data={}, params={}):
  return call('post', path, data, params)

#-------------------------------------------

def patch (path, data={}, params={}):
  return call('patch', path, data, params)

#-------------------------------------------

def delete (path, data={}, params={}):
  return call('delete', path,  params)

#-------------------------------------------

def call (meth, path, data={}, params={}, headers={}):
  global token, username, password, authcode
  result = None
  url = GITHUB_API + path
  data = json.dumps(data)
  log.debug ('Json data: ' + data)

  if meth == 'post' or meth == 'patch':
    headers['Content-type'] = 'application/x-www-form-urlencoded'
  if authcode:
    headers['X-GitHub-OTP'] = authcode
    log.debug('Using authcode.')

  try:
    if token != None:
      params['access_token'] = token
      if meth == 'get':
        request = requests.get( url, params=params, headers=headers )
      if meth == 'post':
        request = requests.post( url, params=params, data=data, headers=headers )
      if meth == 'patch':
        request = requests.patch( url, params=params, data=data, headers=headers )
      if meth == 'delete':
        request = requests.delete( url, params=params, headers=headers )
      log.debug ('API ({0}): {1}'.format(meth, request.url))
    else:
      if meth == 'get':
        request = requests.get( url, auth=(username, password), params=params, headers=headers )
      if meth == 'post':
        request = requests.post( url, auth=(username, password), params=params, data=data, headers=headers )
      if meth == 'patch':
        request = requests.patch( url, auth=(username, password), params=params, data=data, headers=headers )
      if meth == 'delete':
        request = requests.delete( url, auth=(username, password), params=params, headers=headers )
      log.debug ('API ({0}): {1}'.format(meth, request.url))

    _checkStatus( request )

    if meth != 'delete':
      result = json.loads( request.text )
  except Exception as e: 
    print('Oops. We had a slight problem with the GitHub SSO: ' + str( e ))
    sys.exit(0)
  return result

#-------------------------------------------

def auth (username, password):
  global authcode
  log.debug('Authenticating ...')

  url = GITHUB_API + '/authorizations'

  request = requests.get( url, auth=(username, password) )
  log.debug('request.status_code: {0}'.format(request.status_code))
  log.debug('request.text: {0}'.format(request.text))
  log.debug(request.headers)

  # 401 means unsuccessful basic auth
  if request.status_code == 401:
    # check if the OTP header exists... it should
    if 'X-GitHub-OTP' in request.headers:
      log.debug('OTP: {0}'.format( request.headers['X-GitHub-OTP'] ))
      # is OTP required? 
      if request.headers['X-GitHub-OTP'].lower().find('required;') > -1:
        # If sms, request an sms and then prompt for code
        if request.headers['X-GitHub-OTP'].lower().find('sms') > -1:
          print('Requesting SMS from GitHub ...')
          request = requests.post( url, auth=(username, password) )
          log.debug('request.status_code: {0}'.format(request.status_code))
          log.debug('request.text: {0}'.format(request.text))
          log.debug(request.headers)

          if request.status_code == 401:
            authcode = getpass.getpass('Two factor authentication code: ')
          else:
            print('Unable to request SMS from Github')
        # if not sms, assume application, prompt for code
        else:
          log.debug('OTP code did not sms. Assume application...')
          authcode = getpass.getpass('Two factor authentication code: ')
      else:
        log.debug('OTP not required.')
    else:
      print('Github rejected the username and password but didnt send an OTP header. Try again please')
  else:
    # username,pass accepted
    log.debug('Username and password accepted.')

#-------------------------------------------

def _checkStatus (request):
  code = request.status_code
  
  log.debug ('Github API Response Code: %s' % str(code))
  log.debug(request.headers)

  if code == 200 or code == 201 or code == 204:
    pass
  elif code == 404 or code == 403:
    print('Please check your user name and/or password.')
    sys.exit(0)
  elif code == 400:
    print('Bad Request')
    sys.exit(0)
  elif code == 422:
    print('Unprocessable Entity')
    sys.exit(0)
  else:
    print('Uknown Error: ' + str(code))
    sys.exit(0)

