from iosxeapi.iosxerestapi import iosxerestapi
import click
import json


class Device(object):
    def __init__(self, ip=None, port=None, username=None, password=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
    def set_up(self):
        return iosxerestapi(host=self.ip, username=self.username, password=self.password, port=self.port)

@click.group()
# ip addresses or dns of devices
@click.option("--ip",help="ip or dns address of device")
# file of ip addresseses or dns of devices
@click.option("--file",help="file ip addresses of devices")
# option for custom port or uses restconf port 443
@click.option("--port", default=443, help="device port, default = 443" )
# prompts user for name/password of device(s)
@click.option("--username",help="device username", prompt=True, hide_input=False)
@click.option("--password",help="device password", prompt=True, hide_input=True)
@click.pass_context


def main(ctx, ip, file, port, username, password):
    """Gather and Add IOS XE device information using restconf"""
    devices = []
    if ip:
        device = Device(ip, port, username, password)
        devices.append(device)
        click.secho("Working....")
    else:
        try:
            with open(file) as f:
                device_data = json.load(f)
        except (ValueError, IOError, OSError) as err:
            print("Could not read the 'devices' file:", err)

        for device_info in device_data.values():
            ip = device_info['IP']
            device = Device(device_info['IP'], port, username, password)
            devices.append(device)
            click.secho("Working....{}".format(ip))
    ctx.obj = devices


@main.command('get_device')
@click.pass_obj
def get_device(devices):
    """Gather Device information"""
    for device in devices:
        api = device.set_up()
        result = api.get_device()
        print(result)
        click.secho("Task completed")


@main.command('get_bgp')
@click.pass_obj
def get_bgp(devices):
    """Gather BGP information"""
    for device in devices:
        api = device.set_up()
        result = api.get_bgp()
        print(result)
        click.secho("Task completed")


@main.command('get_interfaces')
@click.pass_obj
def get_interfaces(devices):
    """Gather Interface information"""
    for device in devices:
        api = device.set_up()
        result = api.get_interfaces_oper()
        print(result)
        click.secho("Task completed")

@main.command('add_drop')
@click.pass_obj
def add_drop(devices):
    """Add ACL to Interface """
    for device in devices:
        click.secho("Select Interface!")
        router_object = device.set_up()
        list_interfaces = router_object.get_interfaces_list()
        user_interface = click.prompt('Available Interfaces Are:\n' + list_interfaces)
        access = router_object.add_access_group(user_interface)
        print(access.message)
        click.secho("Task completed")

@main.command('delete_drop')
@click.pass_obj
def delete_drop(devices):
    """Remove ACL from Interface """
    for device in devices:
        click.secho("Select Interface!")
        router_object = device.set_up()
        list_interfaces = router_object.get_interfaces_list()
        user_interface = click.prompt('Available Interfaces Are:\n' + list_interfaces)
        delete = router_object.delete_access_group(user_interface)
        print(delete.message)
        click.secho("Task completed")

main()
