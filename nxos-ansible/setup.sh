#! /bin/bash
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir collections
ansible-galaxy collection install cisco.nxos
deactivate