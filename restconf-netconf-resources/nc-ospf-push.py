#! /usr/bin/env python
 
from ncclient import manager
import xmltodict

nc_payload = """ <config>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
  <fm-items>
    <ospf-items>
      <adminSt>enabled</adminSt>
    </ospf-items>
  </fm-items>
  <ospf-items>
    <inst-items>
      <Inst-list>
        <name>1</name>
        <dom-items>
          <Dom-list>
            <name>default</name>
            <ctrl>default-passive</ctrl>
          </Dom-list>
        </dom-items>
      </Inst-list>
    </inst-items>
  </ospf-items>
</System>
</config>
  """

print("Connecting to NXOS device with NETCONF")
with manager.connect(host="10.10.5.240", port="830", username="admin", password="admin", hostkey_verify=False) as m:
  print("Sending NETCONF payload to the Nexus device as edit-config [PATCH verb]")
  nc_response = m.edit_config(target="running", config=nc_payload)
  nc_reply = xmltodict.parse(nc_response.xml)
  transaction_id = list(nc_reply["rpc-reply"].values())[1].split(":")
  print("Configuration: {}.  NETCONF Message ID: {}".format(list(nc_reply["rpc-reply"].keys())[2],transaction_id[2]))