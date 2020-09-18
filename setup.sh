#! /bin/bash
pip install ansible==2.9.12
ansible-playbook sandbox_install.yaml
cd confirm-env && make confirm_env
cd ../
