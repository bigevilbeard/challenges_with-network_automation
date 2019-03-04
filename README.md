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
Once the VIRL simulation is built the follow will be seen.
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

## About me

Network Automation Developer Advocate for Cisco DevNet.
I'm like Hugh Hefner... minus the mansion, the exotic cars, the girls, the magazine and the money. So basically, I have a robe.

Find me here: [LinkedIn](https://www.linkedin.com/in/stuarteclark/) / [Twitter](https://twitter.com/bigevilbeard)
