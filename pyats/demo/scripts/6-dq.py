from genie.testbed import load
tb = load('../testbed.yaml')
dev = tb.devices['dist-sw01']
dev.connect()

# Let's send a command to the device
output = dev.parse('show module')

# Let's get all the rp which are actived
print('All active RP: {}'.format(output.q.contains('active').get_values('rp')))
print('All Ok Linecard: {}'.format(output.q.contains('ok').get_values('lc')))

