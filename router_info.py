from iosxeapi.iosxerestapi import iosxerestapi
from pprint import pprint
import click

# @click.command()
# @click.argument("--ip",help="ip address of device")
# @click.argument("--port",help="device port")
# @click.argument("--username",help="Device username")
# @click.argument("--password",help="Device password")
# @click.argument('--restconf', type=click.Choice(['bgp', 'interfaces']))
#
# def info(ip, port, username, password, restconf):
#     """Gather device information using restconf."""
#     click.secho("Getting information")


router_call = iosxerestapi(host='ios-xe-mgmt.cisco.com', username='root', password='D_Vay!_10&', port=9443)


bgp = router_call.get_bgp()
print(bgp)

intf = router_call.get_interfaces_oper()
print(intf)


# if __name__ == '__main__':
#     info()
