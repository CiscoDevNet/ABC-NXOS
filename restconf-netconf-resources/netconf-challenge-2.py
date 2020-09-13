#! /usr/bin/env python

from ncclient import manager
import xmltodict

loopback = {
  "id": "lo152",
  "ip": "8.8.8.8/32",
  "description": "ADDED VIA NETCONF",
  "process": "1",
  "area": "0.0.0.0",
}

nc_payload = """ <config>
<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
  <ospf-items>
    <inst-items>
      <Inst-list>
        <name>{0}</name>
        <dom-items>
          <Dom-list>
            <name>default</name>
            <if-items>
              <If-list>
                <id>{1}</id>
                <advertiseSecondaries>true</advertiseSecondaries>
                <area>{2}</area>
              </If-list>
            </if-items>
          </Dom-list>
        </dom-items>
      </Inst-list>
    </inst-items>
  </ospf-items>
  <ipv4-items>
    <inst-items>
      <dom-items>
        <Dom-list>
          <name>default</name>
          <if-items>
            <If-list>
              <id>{1}</id>
              <addr-items>
                <Addr-list>
                  <addr>{3}</addr>
                  <pref>0</pref>
                  <tag>0</tag>
                  <type>primary</type>
                </Addr-list>
              </addr-items>
            </If-list>
          </if-items>
        </Dom-list>
      </dom-items>
    </inst-items>
  </ipv4-items>
  <intf-items>
    <lb-items>
      <LbRtdIf-list>
        <id>{1}</id>
        <descr>{4}</descr>
      </LbRtdIf-list>
    </lb-items>
  </intf-items>
</System>
</config>
  """

print("Connecting to NXOS device with NETCONF")
with manager.connect(host="10.10.5.240", port="830", username="admin", password="admin", hostkey_verify=False) as m:
  print("Sending NETCONF payload to the Nexus device as edit-config [PATCH verb]")
  nc_response = m.edit_config(target="running", config=nc_payload.format(loopback["process"], loopback["id"], loopback["area"], loopback["ip"], loopback["description"]))
  nc_reply = xmltodict.parse(nc_response.xml)
  transaction_id = list(nc_reply["rpc-reply"].values())[1].split(":")
  print("Configuration: {}.  NETCONF Message ID: {}".format(list(nc_reply["rpc-reply"].keys())[2],transaction_id[2]))