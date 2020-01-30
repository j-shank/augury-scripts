#!/usr/bin/python3.4
import requests
import argparse
import ast
import json
import sys

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
    parser.add_argument('-s', '--showspecifics', type=bool, help="Print specific relationships", required=False, default=False )
    parser.add_argument('-c', '--showcounts', type=bool, help="Print counts of relationships", required=False, default=False )
    args = parser.parse_args()
    resultid = args.resultid
    showspecifics = args.showspecifics
    showcounts = args.showcounts

    results = get_results(resultid)
    for result in results.splitlines():
        record = json.loads(result)
        srcport = record['src_port']
        dstport = record['dst_port']
        if srcport < dstport:
            tupkey = record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + str(record['proto'])
            tupbrief = record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + record['dst_ip_addr']
        elif dstport < srcport:
            tupkey = record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + str(record['proto'])
            tupbrief = record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + record['src_ip_addr']
        else:
            if hash(record['src_ip_addr']) < hash(record['dst_ip_addr']):
                tupkey = record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + str(record['proto'])
                tupbrief = record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + record['dst_ip_addr']
            else:
                tupkey = record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + record['src_ip_addr'] + '|' + str(record['src_port']) + '|' + str(record['proto'])
                tupbrief = record['dst_ip_addr'] + '|' + str(record['dst_port']) + '|' + record['src_ip_addr']

        tup = (record['tcp_flags'], record['start_time'])
        if tupbrief in tuplefy:
            if tupkey in tuplefy[tupbrief]:
                tuplefy[tupbrief][tupkey].append(tup)
            else:
                tuplefy[tupbrief][tupkey] = [tup]
        else:
            tuplefy[tupbrief] = {}
            tuplefy[tupbrief][tupkey] = [tup] 


    for record in sorted(tuplefy, key=lambda k: len(tuplefy[k]), reverse = True):
        if showcounts == True:
            sys.stdout.write("{0}: {1}\n".format(record, len(tuplefy[record])))
        else:
            sys.stdout.write("{0}\n".format(record))
        if showspecifics == True:
            for tupkey in sorted(tuplefy[record], key=lambda l: len(tuplefy[record][l]), reverse = True):
                if showcounts == True:
                    sys.stdout.write("  - {0}: {1}\n".format(tupkey, len(tuplefy[record][tupkey])))
                else:
                    sys.stdout.write("  - {0}\n".format(tupkey))





