from iosxeapi.iosxerestapi import iosxerestapi
from pprint import pprint
import click


class User(object):
    def __init__(self, ip=None, port=None, username=None, password=None, restconf=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.restconf = restconf

@click.group()
@click.argument("--ip",help="ip address of device")
@click.argument("--port",help="device port")
@click.argument("--username",help="Device username")
@click.argument("--password",help="Device password")
@click.argument('--restconf', type=click.Choice(['bgp', 'interfaces']))

def main(ctx,ip, port, username, password, restconf):
    """Gather device information using restconf."""

    ctx.obj = User(ip,port, username, password, restconf)
    click.secho("Getting information")

@main.command()
@click.pass_obj
def login(ctx):

# router_call = iosxerestapi(host='ios-xe-mgmt.cisco.com', username='root', password='D_Vay!_10&', port=9443)

@main.command()
@click.pass_obj
def get_bgp(ctx):

bgp = router_call.get_bgp()
print(bgp)

@main.command()
@click.pass_obj
def get_interfaces_oper(ctx):

intf = router_call.get_interfaces_oper()
print(intf)


main()
