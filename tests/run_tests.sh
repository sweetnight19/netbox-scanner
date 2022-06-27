#!/bin/sh
#
# Before running these tests, fill the environment variables
# below according to your setup.  If you don't want to
# hardcode this data, just be sure to exporting them in
# your shell.
##

export NETBOX_ADDRESS="172.16.205.130"
export NETBOX_TOKEN="6d922c1b19a4c4cc7bf8f9f20b0fdab6e6e885e9"

export NMAP_PATH="/usr/bin/nmap"

export PRIME_ADDRESS=""
export PRIME_USER=""
export PRIME_PASS=""

export NETXMS_ADDRESS=""
export NETXMS_USER=""
export NETXMS_PASS=""


python -m unittest test_netbox
python -m unittest test_nmap
#python -m unittest test_prime
#python -m unittest test_netxms
