import login
import argparse
import logging
import requests
import hvac
import json
import os
import log
import urllib3

urllib3.disable_warnings()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NXOS Create VLAN')
    parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
    parser.add_argument('--nxos_host', default="https://10.10.20.177", help='the nxos simulator')
    parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
    parser.add_argument('--vlan', required=True, help='the vlan number to create')
    parser.add_argument('--name', required=True, help='the name of the vlan to create')
    args = parser.parse_args()

    # Configure the logger
    logger =  log.default('nxos-vlan-create', level=args.log, patterns=[os.getenv("VAULT_TOKEN")], logfile=None)

    # Get NXOS credentials from our Vault server
    client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
    data = client.read("kv-v1/nxos/bootcamp/nxos-01")
    username = data["data"]["NXOS_USERNAME"]
    password = data["data"]["NXOS_PASSWORD"]
    
    # Create a session for our API requests
    session  = requests.Session()
    response = login.aaa_login(session=session, host=args.nxos_host, username=username, password=password, verify=False)

    # Create a new VLAN
    vlan_response = session.post(f'{args.nxos_host}/api/mo/sys.json', verify=False, json={
	"topSystem": {
		"children": [{
			"bdEntity": {
				"children": [{
					"l2BD": {
						"attributes": {
							"fabEncap": f'vlan-{args.vlan}',
							"name": f'{args.name}'
						}
					}
				}]
			}
		}]
	}
    })
    logger.debug("vlan create response code=%s", vlan_response.status_code)
