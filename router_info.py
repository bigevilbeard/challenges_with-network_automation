from iosxeapi.iosxerestapi import iosxerestapi
from pprint import pprint
import click

@click.command()
@click.option("--ip",help="ip address of device")
@click.option("--port",help="device port")
@click.option("--username",help="Device username")
@click.option("--password",help="Device password")
@click.option('--restconf', type=click.Choice(['bgp', 'interfaces']))

def info(ip, port, username, password, restconf):
    """Gather device information using restconf."""
    click.secho("Getting information")


router_call = iosxerestapi(host='ios-xe-mgmt.cisco.com', username='root', password='D_Vay!_10&', port=9443)


bgp = router_call.get_bgp()
print(bgp)

intf = router_call.get_interfaces_oper()
print(intf)


if __name__ == '__main__':
    info()
