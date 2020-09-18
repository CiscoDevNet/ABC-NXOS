# Installation

Install pyATS|Genie.
```
pip install 'pyats[full]'

git clone https://wwwin-github.cisco.com/DevNet/ABC-NXOS.git
cd ABC-NXOS/pyats
```

OR if you have installed pyATS, please upgrade to latest v20.8.

```
pyats version update
```

# Contents of Pre/Post snapshots

- Pre-snapshots
    - verify_ospf_neighborship
    - verify_advertised_ospf_routes
    - pre_snapshot_ospf
- Post-snapshots
    - verify_ospf_neighborship
    - verify_bgp_neighborship
    - verify_advertised_ospf_bgp_routes
    - post_snapshot_ospf_and_bgp
    - load_snapshots_for_both_pre_and_post
    - snapshot_ospf_comparison
 
# Running for CI/CD session

By pyats run job command
```
pyats run job job.py --testbed-file devnet_sandbox.yaml --trigger-datafile pre_trigger_datafile.yaml --html-logs pre_snapshots

(configure by Ansible)

pyats run job job.py --testbed-file devnet_sandbox.yaml --trigger-datafile post_trigger_datafile.yaml --html-logs post_snapshots
```

HTML report and JSON files (snapshots) will be generated under `pre|post_snapshots` folders.

