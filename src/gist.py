#!/usr/bin/env python

# http://docs.python-requests.org/en/latest/user/quickstart/
# http://www.pythonforbeginners.com/
# http://docs.python.org/2/tutorial/inputoutput.html

import sys, os.path, rest, log

#-------------------------------------------

def list ():
  url = "/gists"
  gists = rest.get(url)
  public_count = 0
  private_count = 0
  for (i, gist) in enumerate(gists):
    private = False
    file_list = ''
    for (file, data) in gist['files'].items():
      file_list += file 
    if gist['public']:
      public_count += 1
    else:
      private_count += 1
    print '{0:4} {1:30} {2:8} {3}'.format(i, file_list, str(gist['public']), gist['description'])
  print "You have %i Gists. (%i Private)" % (len(gists), private_count)

#-------------------------------------------

def new ():
  print "New"

#-------------------------------------------

def update ():
  print "Update"

#-------------------------------------------

def append ():
  print "Append"

#-------------------------------------------

def delete ():
  print "Delete"

#-------------------------------------------

def get ():
  print "Get"

#-------------------------------------------

def main ( args ):
  log.debug ("Arguments " + str( args ))

  cmd = "list" if len(args) == 1 else args[1]

  if cmd in ("token", "t"):
    rest.updateCredentials()
    sys.exit(0)

  rest.getCredentials()

  if cmd in ("list", "l"):
    list()

  if cmd in ("new", "n"):
    new()

  if cmd in ("apped", "a"):
    append()

  if cmd in ("update", "u"):
    update()

  if cmd in ("delete", "d"):
    delete()

  if cmd in ("get", "g"):
    get()

  log.debug ("Done.")

#-------------------------------------------

if __name__ == "__main__":
  if len(sys.argv) == 1:
    log.comment ("No arguments specified, listing your Gists. Try '%s help' if you need help" % sys.argv[0])
  main (sys.argv)

#-------------------------------------------
