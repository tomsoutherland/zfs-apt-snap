#!/usr/bin/env python3

"""
This script assumes all filesystems associated
with the root are contained within or are included
under the root
"""

import re, sys, argparse, os, shlex, datetime, psutil
from subprocess import Popen, PIPE, STDOUT, call
from glob import glob

# delete snapshots older than SNAPPURGE days
SNAPPURGE = 5
# prevent new snaps if last snap is less than SNAPSKIP seconds
SNAPSKIP = 120
SNAP  = "aptsnap"
SNAPT = "%Y-%m-%dT%H%M%S"

def run_command(s, verbose=False):
    pipe = Popen(shlex.split(s), stdout=PIPE, stderr=STDOUT, encoding='utf-8')
    p = pipe.stdout.read()
    pipe.wait(20)
    if verbose:
        print(s, '\n', p)
    if pipe.returncode:
        sys.exit("Failed to run command: " + s + '\n' + p)
    return pipe.returncode, p

def get_root_zfs():
    f = open("/etc/mtab", "r")
    lines = f.readlines()
    for line in lines:
        l = line.split(" ")
        if l[1] == "/":
            return(l[0])
    sys.exit("\nFailed to locat zfs root dataset\n")

Z = get_root_zfs()
verbose = False
timestamp = datetime.datetime.now().strftime(SNAPT)
snapshot_name = "{}_{}".format(SNAP, timestamp)
# get a list of existing snaps
s = "/usr/bin/zfs list -o name -H -t snapshot " + Z
e, snaps = run_command(s, verbose)
skipsnap=1
for snap in snaps.splitlines():
    match = re.search(r'.*aptsnap_(\S+$)', snap)
    now = datetime.datetime.now()
    if match:
        snapobj = datetime.datetime.strptime(match.group(1), SNAPT)
        tdiff = abs(now-snapobj).seconds
        if tdiff < SNAPSKIP:
            skipsnap = 0
if skipsnap:
    s = "/usr/bin/zfs snapshot -r " + Z + "@" + snapshot_name
    e, pipe = run_command(s, verbose)

# prune old snaps
for snap in snaps.splitlines():
    match = re.search(r'.*aptsnap_(\S+$)', snap)
    now = datetime.datetime.now()
    if match:
        snapobj = datetime.datetime.strptime(match.group(1), SNAPT)
        tdiff = abs(now-snapobj).days
        if tdiff > SNAPPURGE:
            s = "/usr/bin/zfs destroy -r " + snap
            e, snaps = run_command(s, verbose)
