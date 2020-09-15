#! /usr/bin/env python
 
from ncclient import manager
import xmltodict

loopbacks = ["lo150", "lo151"]

nc_payload = """ <config>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
    <ospf-items>
    <inst-items>
      <Inst-list>
        <name>1</name>
        <dom-items>
          <Dom-list>
            <name>default</name>
            <if-items>
              <If-list>
                <id>{}</id>
                <advertiseSecondaries>true</advertiseSecondaries>
                <area>0.0.0.0</area>
              </If-list>
            </if-items>
          </Dom-list>
        </dom-items>
      </Inst-list>
    </inst-items>
  </ospf-items>
</System>
</config>
  """

print("Connecting to NXOS device with NETCONF")
with manager.connect(host="10.10.20.177", port="830", username="cisco", password="cisco", device_params={'name': 'nexus'}, hostkey_verify=False) as m:
  print("Sending NETCONF payload to the Nexus device as edit-config [PATCH verb]")
  for loopback in loopbacks: 
    nc_response = m.edit_config(target="running", config=nc_payload.format(loopback))
    nc_reply = xmltodict.parse(nc_response.xml)
    message_id = list(nc_reply["rpc-reply"].values())[0].split(":")
    print("Configuration: {}.  NETCONF Message ID: {}".format(list(nc_reply["rpc-reply"].keys())[2],message_id[2]))