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
# @click.option("--ip", type=click.Choice(["ipaddr", "file"]))
@click.option("--ip",help="ip address of device")
# @click.option("--port",help="Device port")
@click.option("--port", default=443, help="Device port, default 443" )
# @click.option("--username",help="Device username")
# @click.option("--password",help="Device password")
@click.option("--username",help="Device username", prompt=True, hide_input=False)
@click.option("--password",help="Device password", prompt=True, hide_input=True)
@click.pass_context
def main(ctx,ip, port, username, password):
    """Gather and Add IOS XE device information using restconf"""

    ctx.obj = User(ip,port, username, password)
    click.secho("Working....")


@main.command()
@click.pass_obj
def get_bgp(ctx):
    """Gather BGP information"""
    bgp = ctx.set_up().get_bgp()
    print(bgp)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def get_interfaces(ctx):
    """Gather Interface information"""
    intf = ctx.set_up().get_interfaces_oper()
    print(intf)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def get_device(ctx):
    """Gather Device information"""
    dev = ctx.set_up().get_device()
    print(dev)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def add_drop(ctx):
    """Add ACL to Interface """
    click.secho("Select Interface!")
    router_object = ctx.set_up()
    list_interfaces = router_object.get_interfaces_list()
    user_interface = click.prompt('Available Interfaces Are:\n' + list_interfaces)
    access = router_object.add_access_group(user_interface)
    print(access.message)
    click.secho("Task completed")

@main.command()
@click.pass_obj
def delete_drop(ctx):
    """Remove ACL from Interface """
    click.secho("Select Interface!")
    router_object = ctx.set_up()
    list_interfaces = router_object.get_interfaces_list()
    user_interface = click.prompt('Available Interfaces Are:\n' + list_interfaces)
    delete = router_object.delete_access_group(user_interface)
    print(delete.message)
    click.secho("Task completed")

main()
