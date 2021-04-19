#! /usr/bin/env python
"""
Simple Python script leveraging `ncclient`, Jinja2 templates, and network state
as defined in a YAML file declaring intent.
Python script will generate NETCONF payloads using YAML and J2 for each
network device.  NETCONF/XML payload will then be applied to each device
"""

__copyright__ = "Copyright (c) 2020 Cisco Systems, Inc."
__license__ = "MIT"

import yaml
from jinja2 import Template
from ncclient import manager

with open("ospf.j2") as f:
    ospf_template = Template(f.read())
# Loop over network devices to create and deploy network configs
# based on template + intent
    with open("netconf_configs/{}_ospf.cfg".format(device["name"]), "w") as f:
            ospf_config = ospf_template.render(ospf=device["ospf"])
            f.write(ospf_config)
    # Connect to Device with NETCONF
    print("  Connecting to device with NETCONF")
    with manager.connect(host=device["mgmt_address"],
        print("  Sending NETCONF configuration as <edit-config> operation")
        ospf_response = m.edit_config(ospf_config, target = "running")
        time.sleep(2)
        # Handling the XML responses for the configuration actions
        ospf_reply = xmltodict.parse(ospf_response.xml)
        
        ospf_message_id = list(ospf_reply["rpc-reply"].values())[0].split(":")
        # Print configuration replies with the NETCONF message ID
        print("    OSPF Config: {}".format(list(ospf_reply["rpc-reply"].keys())[0]))
        print("      NETCONF Message ID: {}".format(ospf_message_id[2]))
        print("...") 
        
        

