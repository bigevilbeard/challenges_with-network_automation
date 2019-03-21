import requests
import urllib3
import sys
from tabulate import tabulate


# HOST = '172.16.30.66'
# PORT = '443'
# USER = 'cisco'
# PASS = 'cisco'

# HOST = 'ios-xe-mgmt.cisco.com'
# PORT = '9443'
# USER = 'root'
# PASS = 'D_Vay!_10&'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_interfaces():
    url = "https://{h}:{p}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces".format(h=HOST, p=PORT)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
    return response.json()

def main():
    interfaces = get_interfaces()
    # print(interfaces)

    headers = ["Name",
    "Description",
    "VRF",
    "Status",
    "IN-DIS",
    "IN-ERR",
    "OUT-ERR",
    "IN-DIS",
    "IP Address",
    "IN-PKTS",
    "OUT-PKTS"]
    table = list()

    for item in interfaces['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']:
        tr =[item['name'],
        item['description'],
        # item['ipv4'],
        item['vrf'],
        item['admin-status'],
        item['statistics']['in-discards'],
        item['statistics']['in-errors'],
        item['statistics']['out-discards'],
        item['statistics']['out-errors'],
        item['v4-protocol-stats']['in-pkts'],
        item['v4-protocol-stats']['out-pkts']]
        table.append(tr)
        # print(tr)

    print(tabulate(table, headers, tablefmt="fancy_grid"))

if __name__ == '__main__':
    sys.exit(main())
