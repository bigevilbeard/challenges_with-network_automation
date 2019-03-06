#!/usr/bin/env python

##############################################################
# Author: Stuart Clark <stuaclar@cisco.com>
#
#
# python [code].py -ip [ip address]
##############################################################

from napalm import get_network_driver
import argparse
import sys


parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--router_ip", help="Enter device ip address")
args = parser.parse_args()
device_ip = args.router_ip

driver = get_network_driver('ios')
device = driver(username='cisco',
                password='cisco',
                optional_args={'port':22},
                hostname=device_ip)


device.open()
print('Napalm Is Running........')
device.load_merge_candidate(filename='access_group.cfg')
diffs = device.compare_config()


if len(diffs) > 0:
    print(diffs)

    commit = input("Type COMMIT to commit the configuration or hit ENTER to abort: ")
    if commit == 'COMMIT':

        try:
            device.commit_config()


        except Exception as inst:
            print('\nAn error occurred with the commit: ')
            print(type(inst))
            sys.exit(inst)
            print()

        else:
            print('Config committed')

    else:
        sys.exit('Script aborted by user')

else:
    print('No changes needed')
    device.discard_config()

device.close()
