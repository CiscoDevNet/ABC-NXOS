One the power of pyATS, is to make interaction with the device easy, the rest
is just pure Python. No need to learn anything else

There are 4 main APIS to know.

## Connect

connect - Connect to the device

```python
from genie.testbed import load
tb = load('testbed.yaml')

dev = tb.devices['dist-sw01']
dev.connect()
```

That's it!

## Execute

execute - Send commands to the device in enabled mode.
Send command to the device; and returns the string.

```python
from genie.testbed import load
tb = load('testbed.yaml')

dev = tb.devices['dist-sw01']
dev.connect()

# Let's send a command to the device
output = dev.execute('show version')
```

https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/services/generic_services.html#execute


## Configure

configure - Gets your device in `configure terminal` and sends configuration to
the device. Will raise exception when sending Invalid commands and such.

```python
from genie.testbed import load
tb = load('testbed.yaml')

dev = tb.devices['dist-sw01']
dev.connect()

# Let's send a configuration to the device
configuration = '''\
interface Ethernet2/1
shutdown'''

output = dev.configure(configuration)
```

With this, configuration on any device is very easy.


## Parse

parse - This is where things get serious! Take the router information and
transform it into a python dictionary. Once you have the data in a dictionary,
automation can start.

```python
from genie.testbed import load
tb = load('testbed.yaml')

dev = tb.devices['dist-sw01']
dev.connect()

# Let's send the same command but this time work with it
output = dev.parse('show version')
output
```

Let's see what we can do;

## Python and pyATS

```python
from genie.testbed import load
tb = load('testbed.yaml')

dev = tb.devices['dist-sw01']
dev.connect()

# Let's send the same command but this time work with it
output = dev.parse('show interface')
output
```


## Learn

learn - Learn create common models of information about a specific feature.

Ops module provides a representation of the current operational state of a
device, per feature (protocol). It “learns” the operational state by executing
a series of commands and parsing the output into a common data structure across
different operating systems.

The output is stored with the same key-value pair structure across devices and os.


```python
from genie.testbed import load
tb = load('testbed.yaml')

dev = tb.devices['dist-sw01']
dev.connect()

# Let's send the same command but this time work with it
output = dev.learn('ospf')
output.info
```

The same data manipulation can be done here too.

https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models

