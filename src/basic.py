#!/usr/bin/env python

# http://www.pythonforbeginners.com/python-on-the-web/how-to-use-urllib2-in-python/

import urllib2
import base64
import sys

username = sys.argv[1]
password = sys.argv[2]

url = "https://api.github.com/user"

request = urllib2.Request( url )
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   
response = urllib2.urlopen(request)

print( response.info() )
print( response.read() )

response.close()
