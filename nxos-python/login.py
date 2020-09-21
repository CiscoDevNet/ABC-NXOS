import requests
import logging
import hvac
import os
import argparse
import json
import log 
import urllib3

urllib3.disable_warnings()

def aaa_login(host='nxos-01', username='', password='', verify=True, timeout=10, session:requests.Session=None):
    if session == None:
        return requests.post(f'{host}/api/aaaLogin.json', verify=verify, timeout=timeout, json={
            "aaaUser" : {
                "attributes" : {
                    "name" : username,
                    "pwd" : password
                }
            }
        })
    else:
        return session.post(f'{host}/api/aaaLogin.json', verify=verify, timeout=timeout, json={
            "aaaUser" : {
                "attributes" : {
                    "name" : username,
                    "pwd" : password
                }
            }
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NXOS Login')
    parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
    parser.add_argument('--nxos_host', default="https://10.10.20.177", help='nxos 01')
    parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
    args = parser.parse_args()

    logger = log.default("nxos-login", level=args.log, patterns=[os.getenv("VAULT_TOKEN")])
    client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
    data = client.read("kv-v1/nxos/bootcamp/nxos-01")
    username = data["data"]["NXOS_USERNAME"]
    password = data["data"]["NXOS_PASSWORD"]

    # # Issue an API Request to NXOS with missing credentials
    # try:
    #     response = aaa_login(host=args.nxos_host, username="", password="", verify=False)
    #     logger.debug("nxos login status_code=%s", response.status_code)
    # except requests.exceptions.InvalidURL as e:
    #     logger.error("nxos login error=%s", e)

    # # Issue an API Request to the NXOS instance with the wrong host
    # try:
    #     response = aaa_login(host="https://10.10.20.188", username="", password="", verify=False, timeout=2)
    #     logger.debug("nxos login status_code=%s", response.status_code)
    # except requests.exceptions.ConnectTimeout as e:
    #     logger.error("nxos login error=%s", e)

    # # Issue an API Request to the NXOS instance with the wrong credentials
    # response = aaa_login(host=args.nxos_host, username="baduser", password="badpassword", verify=False)
    # logger.debug("nxos login status_code=%s", response.status_code)

    # # Issue an API Request to the NXOS instance with the correct credentials
    # response = aaa_login(host=args.nxos_host, username=username, password=password, verify=False)
    # logger.debug("nxos login status_code=%s", response.status_code)

    # # Log the headers and body of the API response
    # data = response.json()
    # logger.debug("nxos login headers json=%s", json.dumps(dict(response.headers), indent=4))
    # logger.debug("nxos login body json=%s",json.dumps(data, indent=4)) 

    # # Alternatively, establish a session to NXOS 
    # session  = requests.Session()
    # response = aaa_login(session=session, host=args.nxos_host, username=username, password=password, verify=False)
    # logger.debug("nxos login status_code=%s", response.status_code)

    # # Logout
    # logout_response = session.get(f'{args.nxos_host}/api/aaaLogout.json')
    # logger.debug("nxos logout status_code=%s", logout_response.status_code)
