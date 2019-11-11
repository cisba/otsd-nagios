#!/usr/bin/env python3

import requests
import json
import sys

# get status from calendar server
url = sys.argv[1]
headers = {'Accept': 'application/json', 'user-agent': 'otsd-nagios/0.1.0'}

try:
    r = requests.get(url, headers=headers)
except requests.exceptions.RequestException as error:
    print("UNKNOWN: http call error = %s" % error)
    sys.exit(3)

if r.status_code is not 200:
    print("UNKNOWN: http status code = %d" % r.status_code)
    sys.exit(3)

# parse json response
try:
    status = r.json()
except:
    print("UNKNOWN: error parsing json response (%s)" % r.text)
    sys.exit(3)

# dump for debug
#print(json.dumps(r.json(), indent=2))

# evaluate balance
DUST = 0.001 # This value is too high, and has to be changed server side!
CRITICAL_BALANCE = DUST
WARNING_BALANCE = 100*DUST

balance = float(status["balance"])
if balance < CRITICAL_BALANCE:
    print("CRITICAL | Balance=%fBTC" % balance)
    sys.exit(2)
elif balance < WARNING_BALANCE:
    print("WARNING | Balance=%fBTC" % balance)
    sys.exit(1)

print("OK | Balance=%fBTC" % balance)


