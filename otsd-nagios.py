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
    # request exception is a client error, server status is unknown
    print("UNKNOWN: http call error = %s" % error)
    sys.exit(3)

if r.status_code >= 500:
    # http 5xx is a server side error
    print("CRITICAL: http status code = %d" % r.status_code)
    sys.exit(2)
elif r.status_code >= 400:
    # http 4xx is a client error, server status is unknown
    print("UNKNOWN: http status code = %d" % r.status_code)
    sys.exit(3)
elif r.status_code is not 200:
    # http status != 200 is assumed as a server warning
    print("WARNING: http status code = %d" % r.status_code)
    sys.exit(1)

# parse json response
try:
    status = r.json()
except:
    # parsing error could be caused by client, server status is unknown
    print("UNKNOWN: error parsing json response (%s)" % r.text)
    sys.exit(3)

# dump for debug
#print(json.dumps(r.json(), indent=2))

# evaluate balance
# https://github.com/bitcoin/bitcoin/blob/master/src/policy/policy.cpp
DUST = 0.00000546
CRITICAL_BALANCE = DUST
WARNING_BALANCE = 100 * DUST

balance = float(status["balance"])
if balance < CRITICAL_BALANCE:
    print("CRITICAL | Balance=%fBTC" % balance)
    sys.exit(2)
elif balance < WARNING_BALANCE:
    print("WARNING | Balance=%fBTC" % balance)
    sys.exit(1)

print("OK | Balance=%fBTC" % balance)


