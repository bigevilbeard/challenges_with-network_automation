import requests
import urllib3
import sys
from tabulate import tabulate


HOST = '172.16.30.66'
PORT = '443'
USER = 'cisco'
PASS = 'cisco'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bgp():
    url = "https://{h}:{p}/restconf/data/Cisco-IOS-XE-bgp-oper:bgp-state-data".format(h=HOST, p=PORT)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
    return response.json()
    # print(response)

def main():
    neighbors = get_bgp()
    # print(neighbors)

    headers = ["Neighbor", "LINK", "UP-TIME", "STATE", "PfxRcd" ]
    table = list()

    for item in neighbors['Cisco-IOS-XE-bgp-oper:bgp-state-data']['neighbors']['neighbor']:
        tr = [item['neighbor-id'],
        item['link'],
        item['up-time'],
        item['connection']['state'],
        item['prefix-activity']['received']['total-prefixes']]
        table.append(tr)
        # print(tr)

    print(tabulate(table, headers, tablefmt="fancy_grid"))

if __name__ == '__main__':
    sys.exit(main())
