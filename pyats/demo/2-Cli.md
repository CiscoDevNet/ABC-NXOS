# 3. Automation for non-programmer

We are providing simple linux CLI to interact with our libraries. No need to
know Python, just use the cli and a testbed yaml file and you can do:

* Connect to the devices
* Execute commands on the devices
* Parse devices outputs
* Learn devices features

Let's think of a few usecases:

* Take snapshot of a network with the help of parser/learn
* Compare snapshots to see what has changed
* Run on a schedule with a Cron job, jenkins, 

Let's investigate

pyats parse "show version" --testbed-file testbed.yaml --output snap1
pyats learn "ospf" --testbed-file testbed.yaml --output snap1

pyats diff snap1 snap2

