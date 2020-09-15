#! /usr/bin/env python
"""
Author: Quinn Snyder <qsnyder@cisco.com>
nc_push.py
Simple Python script leveraging `ncclient`, Jinja2 templates, and network state
as defined in a YAML file declaring intent.
Python script will generate NETCONF payloads using YAML and J2 for each
network device.  NETCONF/XML payload will then be applied to each device
"""

__author__ = ("Quinn Snyder")
__author_email__ = ("qsnyder@cisco.com")
__copyright__ = "Copyright (c) 2020 Cisco Systems, Inc."
__license__ = "MIT"

import yaml
from jinja2 import Template
from ncclient import manager
import xmltodict
import time

# Loads the network configuration intent
print("Gathering intended network configuration from YAML")
with open("intent.yaml") as f:
    config = yaml.safe_load(f.read())

# Create Jinja Template Objects for NETCONF Payloads
print("Setting Up NETCONF Jinja2 templates")
print("...")
print("")

# OSPF routing configuration
with open("ospf.j2") as f:
    ospf_template = Template(f.read())

# Layer 3 interface configurations
with open("interfaces.j2") as f:
    interface_template = Template(f.read())

# Loopback interface configurations
with open("loopbacks.j2") as f:
    loopback_template = Template(f.read())

# Loop over network devices to create and deploy network configs
# based on template + intent
print("Processing Device Configurations")
for device in config["devices"]:
    print("Device: {}".format(device["name"]))
    # Building device specific templates
    print("  Creating device specific configurations from templates + intent")
    with open("netconf_configs/{}_ospf.cfg".format(device["name"]), "w") as f:
        ospf_config = ospf_template.render(ospf=device["ospf"])
        f.write(ospf_config)
    with open("netconf_configs/{}_interface.cfg".format(device["name"]), "w") as f:
        interfaces = interface_template.render(interfaces=device["interfaces"])
        f.write(interfaces)
    with open("netconf_configs/{}_loopback.cfg".format(device["name"]), "w") as f:
        loopbacks = loopback_template.render(loopbacks=device["loopbacks"])
        f.write(loopbacks)

    # Connect to Device with NETCONF
    print("  Connecting to device with NETCONF")
    with manager.connect(host=device["mgmt_address"],
                         port=device["netconf_port"],
                         username=config["username"],
                         password=config["password"],
                         hostkey_verify=False,
                         device_params={'name': 'nexus'},
                         allow_agent=False,
                         look_for_keys=False) as m:

        # Send NETCONF Configurations with <edit-config> RPC
        print("  Sending NETCONF configuration as <edit-config> operation")
        ospf_response = m.edit_config(ospf_config, target = "running")
        time.sleep(2)
        interface_response = m.edit_config(interfaces, target = "running")
        time.sleep(2)
        loopback_response = m.edit_config(loopbacks, target = "running")
        time.sleep(2)

        # Handling the XML responses for the configuration actions
        ospf_reply = xmltodict.parse(ospf_response.xml)
        interface_reply = xmltodict.parse(interface_response.xml)
        loopback_reply = xmltodict.parse(loopback_response.xml)
        #adminup_message_id = list(adminup_reply["rpc-reply"].values())[5].split(":")
        ospf_message_id = list(ospf_reply["rpc-reply"].values())[5].split(":")
        interface_message_id = list(interface_reply["rpc-reply"].values())[5].split(":")
        loopback_message_id = list(loopback_reply["rpc-reply"].values())[5].split(":")
        
        # Print configuration replies with the NETCONF message ID
        print("    OSPF Config: {}".format(list(ospf_reply["rpc-reply"].keys())[6]))
        print("      NETCONF Message ID: {}".format(ospf_message_id[2]))
        print("    Interface Config: {}".format(list(interface_reply["rpc-reply"].keys())[6]))
        print("      NETCONF Message ID: {}".format(interface_message_id[2]))
        print("    Loopback Config: {}".format(list(loopback_reply["rpc-reply"].keys())[6]))
        print("      NETCONF Message ID: {}".format(loopback_message_id[2]))
        print("...")