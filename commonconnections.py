#!/usr/bin/python3.4
import requests
import argparse
import ast
import json



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
    r1addrs = {}
    r2addrs = {}
    parser = argparse.ArgumentParser(description="Fetches Augury results.")
    parser.add_argument('-r', '--resultid1', type=int, help="Result ID 1 to fetch.", required=True, default=None )
    parser.add_argument('-t', '--resultid2', type=int, help="Result ID 2 to fetch.", required=True, default=None )
    args = parser.parse_args()
    resultid1 = args.resultid1
    resultid2 = args.resultid2

    results = get_results(resultid1)
    for result in results.splitlines():
        record = json.loads(result)
        r1addrs[record['src_ip_addr']] = r1addrs.get(record['src_ip_addr'], 0) + 1
        r1addrs[record['dst_ip_addr']] = r1addrs.get(record['dst_ip_addr'], 0) + 1

    results2 = get_results(resultid2)
    for result2 in results2.splitlines():
        record = json.loads(result2)
        r2addrs[record['src_ip_addr']] = r2addrs.get(record['src_ip_addr'], 0) + 1
        r2addrs[record['dst_ip_addr']] = r2addrs.get(record['dst_ip_addr'], 0) + 1

    keys_r1 = set(r1addrs.keys())
    keys_r2 = set(r2addrs.keys())
    intersection = keys_r1 & keys_r2
    for addr in intersection:
        print("{0}: count1({1}), count2({2}), total({3})".format(addr, r1addrs[addr], r2addrs[addr], r1addrs[addr] + r2addrs[addr]))




