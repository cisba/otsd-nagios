#!/usr/bin/env python3

import requests
import json
import sys

# get status from calendar server
headers = {'Accept': 'application/json', 'user-agent': 'otsd-nagios/0.1.0'}
url = 'https://otsdev.int4mind.com'
r = requests.get(url, headers=headers)
if r.status_code is not 200:
    print("UNKNOWN: http status code = %d" % r.status_code)
    sys.exit(3)

# parse json response
try:
    status = r.json()
except:
    print("UNKNOWN: error parsing json response (%s)" % r.text)
    sys.exit(3)

# evaluate status
print("OK | Balance=%sBTC" % status["balance"])

# dump for debug
print(json.dumps(r.json(), indent=2))
