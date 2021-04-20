# Device Connection

## Testbed

A testbed file contains all the information related to your devices.

1. Device hostname
2. Device credentials
3. Device OS
4. How to connect to the device (Ip/protocol)


```
devices:
  dist-sw01:               <-- Device configured Hostname
    os: nxos                   <-- Device OS
    credentials:               <-- Credentials
      default:
        password: cisco
        username: cisco
    connections:               <-- How to connect to the device
      ssh:                         <-- Connection name
        ip: 10.10.20.177
        protocol: ssh
    type: nxos
```

Run the following command to help you to create it with Multiplatform Network devices
Incase you make a mistake 

```
  mv testbed.yaml testbedold.yaml
```

```
pyats create testbed interactive --output testbed.yaml
```

Run the following command to validate the testbed

```
pyats validate testbed testbed.yaml
```

Testbed file contains many other features, but let's keep at this for now.

## Connect

Once we have our Testbed file, let's connect to our device

pyats parse "show version" --testbed-file testbed.yaml --output snap1

```python
from genie.testbed import load
tb = load('testbed.yaml')
dev = tb.devices['dist-rtr01']
dev.connect()
# Let's send a command to the device
output = dev.execute('show ip route')
```

That is it,  end of the first section. As an exercise; let's add another
device and also connect to this device.
