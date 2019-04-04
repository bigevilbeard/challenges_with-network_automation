import requests
import urllib3
import sys
import argparse
from tabulate import tabulate


# HOST = '172.16.30.66'
# PORT = '443'
# USER = 'cisco'
# PASS = 'cisco'

HOST = 'ios-xe-mgmt.cisco.com'
PORT = '9443'
USER = 'root'
PASS = 'D_Vay!_10&'



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_info():
    url = "https://{h}:{p}/restconf/data/Cisco-IOS-XE-native:native".format(h=HOST, p=PORT)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
    return response.json()
    # print(response)

def main():
    system = get_info().get("Cisco-IOS-XE-native:native")
    # print(system)

    headers = ["Hostname",
    "Version"]
    table = list()

    hostname = system.get('hostname')
    version = system.get('version')
    table.append((hostname, version))

    print(tabulate(table, headers, tablefmt="fancy_grid"))

if __name__ == '__main__':
    sys.exit(main())
