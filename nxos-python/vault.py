import sys
import argparse
import logging
import requests
import hvac
import json
import os
import log

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vault Init')
    parser.add_argument('--vault', default="http://10.10.20.50:1234", help='the vault server')
    parser.add_argument('--log', default="DEBUG", help="logging level [FATAL, ERROR, WARN, INFO, DEBUG]")
    args = parser.parse_args()
    logger = log.default("nxos-vault", patterns=[os.getenv("VAULT_TOKEN")])
    logger.info(os.environ)
    logger.info("running vault examples")
    client = hvac.Client(args.vault, os.getenv("VAULT_TOKEN"))
    data = client.read("kv-v1/nxos/bootcamp/nxos-01")
    logger.info(msg="nxos bootcamp data", extra={'json': data})
    logger.info(data["data"]["NXOS_USERNAME"])
    logger.info(data["data"]["NXOS_PASSWORD"])
