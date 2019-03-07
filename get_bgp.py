import requests
import urllib3
import sys
from tabulate import tabulate


HOST = '172.16.30.65'
PORT = '443'
USER = 'cisco'
PASS = 'cisco'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_configured_interfaces():
    url = "https://{h}:{p}//restconf/data/Cisco-IOS-XE-bgp-common-oper".format(h=HOST, p=PORT)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    response = requests.get(url, auth=(USER, PASS), headers=headers, verify=False)
    return response.json()

def main():
    interfaces = get_configured_interfaces()
    # print(type(interfaces))
    print(interfaces)

    # headers = ["Host Name", "Description", "Status", "IP Address", "Mask"]
    # table = list()
    #
    # for item in interfaces['ietf-interfaces:interfaces']['interface']:
    #     tr = [item['name'],
    #     item ['description'],
    #     item['enabled'],
    #     item['ietf-ip:ipv4']['address'][0]['ip'],
    #     item['ietf-ip:ipv4']['address'][0]['netmask']]
    #     table.append(tr)
    #     # print(tr)
    #
    # print(tabulate(table, headers, tablefmt="fancy_grid"))

if __name__ == '__main__':
    sys.exit(main())
