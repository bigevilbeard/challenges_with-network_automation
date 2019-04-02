# Challenges With Network Automation

## DevNet Sandbox
All code has been tested on the Cisco DevNet Multi-IOS Cisco Test Network Sandbox [HERE](https://devnetsandbox.cisco.com/RM/Diagram/Index/6b023525-4e7f-4755-81ae-05ac500d464a?diagramType=Topology).

Please see the sandbox pages for credentials and reservations. This demo example is based on Python 3.6 and was tested successfully under that version.


## Code

All of the code and examples for this are located in this directory. Clone and access it with the following commands:

```
git clone https://github.com/bigevilbeard/challenges_with-network_automation.git
cd challenges_with-network_automation
```

## Python Environment Setup
It is recommended that this demo be completed using Python 3.6.

It is highly recommended to leverage Python Virtual Environments for completing exercises in this course.

Follow these steps to create and activate a venv.
```
# OS X or Linux
virtualenv venv --python=python3.6
source venv/bin/activate
```
## Install the code requirements
```
pip install -r requirements
```

## Reservation Setup
This lesson leverages a specific [VIRL](https://github.com/bigevilbeard/challenges_with-network_automation/blob/master/topology.virl) topology. Before beginning this lesson run the following command to reconfigure the Sandbox with the proper topology.

From the `challenges_with-network_automation` directory
```
# Get a list of currently running simulations
virl ls --all

# Stop any running simulations.
virl down --sim-name API-Test

# Start the VIRL Simulation for demo
virl up

# Monitor status of simulation
virl nodes   # Node startup
```
Once the VIRL simulation is built, the following will be seen.
```
(venv) [developer@devbox challenges_with-network_automation]$virl ls
Running Simulations
╒═══════════════════════════════════════════════════╤══════════╤════════════════════════════╤═══════════╕
│ Simulation                                        │ Status   │ Launched                   │ Expires   │
╞═══════════════════════════════════════════════════╪══════════╪════════════════════════════╪═══════════╡
│ challenges_with-network_automation_default_yNccAp │ ACTIVE   │ 2019-03-04T16:19:46.778031 │           │
╘═══════════════════════════════════════════════════╧══════════╧════════════════════════════╧═══════════╛
```

NOTE: IP addresses will differ in your own simulation

```
(venv) [developer@devbox challenges_with-network_automation]$virl nodes
Here is a list of all the running nodes
╒═══════════╤══════════╤═════════╤═════════════╤════════════╤══════════════════════╤════════════════════╕
│ Node      │ Type     │ State   │ Reachable   │ Protocol   │ Management Address   │ External Address   │
╞═══════════╪══════════╪═════════╪═════════════╪════════════╪══════════════════════╪════════════════════╡
│ PE-2      │ CSR1000v │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.91         │ N/A                │
├───────────┼──────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ PE-1      │ CSR1000v │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.90         │ N/A                │
├───────────┼──────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ CE-1      │ CSR1000v │ ACTIVE  │ REACHABLE   │ telnet     │ 172.16.30.89         │ N/A                │
├───────────┼──────────┼─────────┼─────────────┼────────────┼──────────────────────┼────────────────────┤
│ ~mgmt-lxc │ mgmt-lxc │ ACTIVE  │ REACHABLE   │ ssh        │ 172.16.30.87         │ 172.16.30.88       │
╘═══════════╧══════════╧═════════╧═════════════╧════════════╧══════════════════════╧════════════════════╛
```

## Running the code examples

Configuration is done using the Representational State Transfer Configuration Protocol (RESTCONF). RESTCONF is an HTTP based protocol. It provides a programmatic interface based on standard mechanisms for accessing configuration data, state data, data-model-specific Remote Procedure Call (RPC) operations and events defined in a YANG model. This code is using native YANG models for IOS-XE - models that are specific to IOS-XE platforms.

- `get_bgp.py` - Passes static configuration IP Address/Port/User/Password and will get all device BGP information. Results are printed using [Tabulate](https://pypi.org/project/tabulate/)
- `get_interfaces.py` - Passes static configuration IP Address/Port/User/Password and will get all device interface information. Results are printed using [Tabulate](https://pypi.org/project/tabulate/)
- `get_device.py` - Passes static configuration IP Address/Port/User/Password and will get device hostname and version information. Results are printed using [Tabulate](https://pypi.org/project/tabulate/)

- `router_info.py` - This code uses Object-Oriented Programming (OOP). This is a programming paradigm where different components of a computer program are modeled after real-world objects. An object is anything that has some characteristics and can perform a function. All args used in the running of the code are handled using [CLICK](https://click.palletsprojects.com/en/7.x/). Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.

In this code, we can show the router BGP and interface information (shown in `json` format). We can also add an access list to an interface with the `patch` and `delete`. As with REST, with RESTCONF we can use Methods. Methods are `HTTPS` operations _`(GET/PATCH/POST/DELETE/OPTIONS/PUT)`_ performed on a target resource.

Use the `--help` to see the Options and Commands

```
(venv) STUACLAR-M-R6EU:challenges_with-network_automation stuaclar$ python router_info.py --help
Usage: router_info.py [OPTIONS] COMMAND [ARGS]...

  Gather and Add IOS XE device information using restconf

Options:
  --ip TEXT        ip address of device
  --port INTEGER   Device port, default 443
  --username TEXT  Device username
  --password TEXT  Device password
  --help           Show this message and exit.

Commands:
  add_drop        Add ACL to Interface
  delete_drop     Remove ACL from Interface
  get_bgp         Gather BGP information
  get_device      Gather Device information
  get_interfaces  Gather Interface information
```
## Guest Shell on CE-1

```
host-CE-1(config)#iox
host-CE-1(config)#
*Mar 21 10:56:58.177: %UICFGEXP-6-SERVER_NOTIFIED_START: R0/0: psd: Server iox has been notified to start
host-CE-1(config)#end
```
Confirm IOX is Running

```
host-CE-1#sh iox
Virtual Service Global State and Virtualization Limits:

Infrastructure version : 1.7
Total virtual services installed : 0
Total virtual services activated : 0

Machine types supported   : KVM, LXC
Machine types disabled    : none

Maximum VCPUs per virtual service : 0
Resource virtualization limits:
Name                         Quota     Committed     Available
--------------------------------------------------------------
system CPU (%)                   7             0             7
memory (MB)                   1024             0           882
bootflash (MB)               20000             0          6719


IOx Infrastructure Summary:
---------------------------
IOx service (CAF)    : Running
IOx service (HA)     : Not Running
IOx service (IOxman) : Running
Libvirtd             : Running
```
Enable Guest Shell
```
host-CE-1#guestshell enable
Interface will be selected if configured in app-hosting
Please wait for completion
....

```

## Add the python script via bash

```
host-CE-1#guestshell run bash
[guestshell@guestshell ~]$touch bgp_down.py
[guestshell@guestshell ~]$ vi bgp_down.py
<esc>, i
import sys
import cli


print "\n\n *** Shutting Down BGP Session  *** \n\n"
cli.configurep(["router bgp 100","neighbor 10.1.2.2 shutdown", "end"])
<esc>, wq
```

## About me

Network Automation Developer Advocate for Cisco DevNet.
I'm like Hugh Hefner... minus the mansion, the exotic cars, the girls, the magazine and the money. So basically, I have a robe.

Find me here: [LinkedIn](https://www.linkedin.com/in/stuarteclark/) / [Twitter](https://twitter.com/bigevilbeard)
