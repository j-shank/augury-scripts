#!/usr/bin/python3.4
import requests
import argparse
import ast
import json
import sys
import socket
import errno

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)



def get_results(resultid):

    url = "https://augury5.cymru.com/api/results/{id}?format=json".format(id=resultid)

    payload = ""
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Token JSHANK-GITHUB-SCRIPTS-REPLACE-THIS-WITH-YOUR-TOKEN"
        }

    response = requests.request("GET", url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Fetch failed, returning code {0} for id {1}\nurl: {2}\n\n{3}".format(response.status_code, resultid, url, response.json()))


if __name__ == "__main__":
    tuplefy = {}
    parser = argparse.ArgumentParser(description="Fetches Augury results.")
    parser.add_argument('-r', '--resultid', type=int, help="Result ID to fetch.", required=True, default=None )
    args = parser.parse_args()
    resultid = args.resultid

    results = get_results(resultid)
    for result in results.splitlines():
        record = json.loads(result)
        srcport = record['src_port']
        dstport = record['dst_port']
        if srcport < dstport:
            tupkey = record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + str(record['proto'])
        elif dstport < srcport:
            tupkey = record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + str(record['proto'])
        else:
            if hash(record['src_ip_addr']) < hash(record['dst_ip_addr']):
                tupkey = record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + str(record['proto'])
            else:
                tupkey = record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + str(record['proto'])



        tup = (record['tcp_flags'], record['start_time'])
        if tupkey in tuplefy:
            tuplefy[tupkey].append(tup)
        else:
            tuplefy[tupkey] = [tup] 


    for record in sorted(tuplefy, key=lambda k: len(tuplefy[k]), reverse = True):
        sys.stdout.write("{0}: {1}\n".format(record, len(tuplefy[record])))




