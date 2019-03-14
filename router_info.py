from iosxeapi.iosxerestapi import iosxerestapi
from pprint import pprint
import click


class User(object):
    def __init__(self, ip=None, port=None, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
    def set_up(self):
        return iosxerestapi(host=self.ip, username=self.username, password=self.password, port=self.port)

@click.group()
@click.option("--ip",help="ip address of device")
@click.option("--port",help="device port")
@click.option("--username",help="Device username")
@click.option("--password",help="Device password")
@click.pass_context
def main(ctx,ip, port, username, password):
    """Gather device information using restconf."""

    ctx.obj = User(ip,port, username, password)
    click.secho("Getting information")


@main.command()
@click.pass_obj
def get_bgp(ctx):
    bgp = ctx.set_up().get_bgp()
    print(bgp)

@main.command()
@click.pass_obj
def get_interfaces_oper(ctx):
    intf = ctx.set_up().get_interfaces_oper()
    print(intf)


main()
