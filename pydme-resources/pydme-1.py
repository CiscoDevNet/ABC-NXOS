from pydme import *
import time

n9k1 = Node('https://10.10.20.58', verify=False, disableWarnings=True)


interfaces = ['eth1/10', 'eth1/11', 'eth1/12']

segments = [['192.168.12.', '192.168.13.', '192.168.14.']]

switch_mit = []

n9k1.methods.Login('admin', password='Cisco123').POST()
n1_mit = n9k1.mit
n1_ts = n1_mit.topSystem()
switch_mit.append(n1_mit)


for switch in switch_mit:
  ospf_feature = switch.topSystem().fmEntity().fmOspf(adminSt='enabled')
  ospf_entity = switch.topSystem().ospfEntity()
  ospf_entity.adminSt = 'enabled'
  ospf_inst = ospf_entity.ospfInst(name='1')
  ospf_feature.POST()
  ospf_entity.POST()
print("=> Configuring all devices to enable OSPF feature")

for switch in switch_mit:
  names = switch.topSystem()
  for interface in interfaces:
    l3_int = switch.topSystem().interfaceEntity().l1PhysIf(id=interface, layer='Layer3', adminSt='up')
    int_ospf = switch.topSystem().ospfEntity().ospfInst(name='1').ospfDom(name='default').ospfIf(area='0.0.0.0', id=interface)
    switch.topSystem().POST()
print("=> Turning up layer-3 interfaces on all devices, enable OSPF")

for id, switch in enumerate(switch_mit,10):
  l_id = str(id)
  loopback_int = switch.topSystem().interfaceEntity().l3LbRtdIf(id='lo0')
  loopback_ip = switch.topSystem().ipv4Entity().ipv4Inst().ipv4Dom(name='default').ipv4If(id='lo0').ipv4Addr(addr=l_id + "." + l_id + "." + l_id + "." + l_id + '/32')
  loopback_ospf = switch.topSystem().ospfEntity().ospfInst(name='1').ospfDom(name='default').ospfIf(area='0.0.0.0', id='lo0')
  switch.topSystem().POST()
print("=> Enabled, IP'd, OSPF'd loopbacks on all devices")

for switchid, switch in enumerate(switch_mit):
  end_ip = str(switchid + 1)
  for linkid, interface in enumerate(interfaces):
    ip_address = switch.topSystem().ipv4Entity().ipv4Inst().ipv4Dom(name='default').ipv4If(id=interface).ipv4Addr(addr=segments[switchid][linkid] + end_ip + "/24")
    switch.topSystem().POST()
print("=> Enabled IP addresses on all routed interfaces")
print("=> Pausing for 30 seconds for routing to converge")
time.sleep(30)
print("=> Success!")
