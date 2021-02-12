#!/usr/bin/python

import os
import subprocess
from subprocess import call
from cisco import system

BASEDIR = os.path.dirname(os.path.realpath(__file__))
CFGDIR = os.path.join(BASEDIR, "config-backup")
HOSTNAME = system.System().get_hostname()

if not os.path.isdir(os.path.join(CFGDIR, HOSTNAME)):
    os.mkdir(os.path.join(CFGDIR, HOSTNAME))

os.chdir(CFGDIR)

call(
    [
        "cp",
        "/bootflash/running.latest",
        "{}/{}/running.latest".format(CFGDIR, HOSTNAME),
    ]
)
call(
    [
        "git",
        "add",
        "{}/{}/running.latest".format(CFGDIR, HOSTNAME),
    ]
)
call(["git", "commit", "-m", "Configuration change"])
p = subprocess.Popen(
    [
        "chvrf",
        "management",
        "git",
        "push",
        "http://root:C1sco12345@10.10.20.50/root/config-backup.git",
        "--all",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
out, err = p.communicate()

with open(os.path.join(BASEDIR, "output.log"), "a+") as f:
    f.write(out)
    f.write(err)