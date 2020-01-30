#!/usr/bin/python3.4
import requests
import json
#import base64
import time
import argparse
import sys
from datetime import datetime, timedelta

endtime = datetime.today()
formattedend = endtime.strftime("%m/%d/%Y 23:59:59")


parser = argparse.ArgumentParser(description="Creates an Augury query for flows and PDNS.")
parser.add_argument('-d', '--deltadays', type=int, help="How many days to query? (all queries include today)", required=False, default=30 )
parser.add_argument('-n', '--queryname', type=str, help="What should we call this query?", required=True, default=None )
parser.add_argument('-x', '--querydescription', type=str, help="What description should be associated with this query?", required=False, default='' )
args = parser.parse_args()
deltadays = args.deltadays
queryname = args.queryname
querydesc = args.querydescription

starttime = endtime - timedelta(days=deltadays)
formattedstart = starttime.strftime("%m/%d/%Y 00:00:00")

inputset = set()

for line in sys.stdin:
    inputset.add(line.rstrip())

cidrs = ",".join(inputset)

url = "https://augury5.cymru.com/api/jobs"
payload = {
        'job_name': queryname,
        'job_description': querydesc,
        'start_date': formattedstart,
        'end_date': formattedend,
        'queries' : [
            {
                'query_type':'flows',
                'any_ip_addr': cidrs
            },
            {
                'query_type':'pdns',
                'any_ip_addr':cidrs
            }
        ]
    }

headers = {
    'Content-Type': "application/json",
    'Authorization': "Token JSHANK-GITHUB-SCRIPTS-REPLACE-THIS-WITH-YOUR-TOKEN"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
if response.status_code == 200:
    json_data = response.json()
    #print(response.json())
    idnum = json_data['job']['id']
    print('Successfully submitted, job id: ' + str(idnum))
    
else:
    print('Error Code: ' + response.status_code)
    print(response.text)
                                
