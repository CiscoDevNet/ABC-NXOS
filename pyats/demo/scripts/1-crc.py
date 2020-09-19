
from genie.testbed import load
tb = load('../testbed.yaml')
dev = tb.devices['dist-sw01']
dev.connect()

# Let's send a command to the device
output = dev.parse('show interface')

# Structure looks like
#interface
#  counters
#     in_crc_errors

for interface in output:
    if 'counters' in output[interface] and\
       'in_crc_errors' in output[interface]['counters']:
        crc_error = output[interface]['counters']['in_crc_errors']
        if crc_error > 0:
            print("Interface '{intf}' has '{error}' "
                  "crc_error".format(intf=interface,
                                     error=crc_error))
        else:
            print("Interface '{intf}' has '{error}' "
                  "crc_error".format(intf=interface,
                                     error=crc_error))

