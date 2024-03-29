import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# disable any ssl insecure warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Assign requests.Session instance to session variable
session = requests.Session()

# Define URL and PAYLOAD variables
URL = "https://10.10.20.177/api/aaaLogin.json"
PAYLOAD = {
          "aaaUser": {
            "attributes": {
              "name": "cisco",
              "pwd": "cisco"
               }
            }
          }

# Obtain an authentication cookie
session.post(URL,json=PAYLOAD,verify=False)

# Define SYS_URL variable
SYS_URL = "https://10.10.20.177/api/mo/sys.json"

# Obtain system information by making session.get call
# then convert it to JSON format then filter to system attributes
sys_info = session.get(SYS_URL).json()["imdata"][0]["topSystem"]["attributes"]

# Print hostname, serial nmber, uptime and current state information
# obtained from the NXOSv9k
print("HOSTNAME:", sys_info["name"])
print("SERIAL NUMBER:", sys_info["serial"])
print("UPTIME:", sys_info["systemUpTime"])

# Define USR_URL and USR_PAYLOAD variables
# TO DO Challenge 
# Add JSON Payload and URI to add vlan 500 
# Vlan name = vlan-500
# Add New Code Below




    
			
# Create a user with REST API's POST method
vlan_create = session.post(USR_URL, json=USR_PAYLOAD,verify=False)

# Check if creation was successful and if yes print such message
if vlan_create.ok:
    print("VLAN WAS SUCCESSFULLY CREATED!")
