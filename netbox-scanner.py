#!/usr/bin/env python3

##################################################
# Author:  José Lopes (Iopes)
# Copyright: Copyright 2022, Netbox-Scanner
# License: MIT
# Version: 1.0.1
# Maintainer: David Marquet
# Email: david.marquet@salle.url.edu
# Status: Development
##################################################

import logging
import sys
import os

from configparser import ConfigParser
from os.path import expanduser, isfile
from datetime import datetime
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from nbs import NetBoxScanner
from nbs.nmap import Nmap


directory = os.path.dirname(sys.argv[0])


def initScript():
    local_config = expanduser(directory+'/netbox-scanner.conf')
    config = ConfigParser()

    if isfile(local_config):
        print('Using local config: ' + local_config)
        config.read(local_config)
    else:
        raise FileNotFoundError('Configuration file was not found.')

    global netbox
    netbox = config['NETBOX']
    global nmap
    nmap = config['NMAP']

    logfile = directory+'/{}/netbox-scanner-{}.log'.format(
        netbox['logs'],
        datetime.now().isoformat()
    )
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format='%(asctime)s\tnetbox-scanner\t%(levelname)s\t%(message)s'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

    # useful if you have tls_verify set to no
    disable_warnings(InsecureRequestWarning)


def cmd_nmap(s):  # nmap handler
    h = Nmap(directory+"/"+nmap['path'], nmap['unknown'])
    h.run()
    s.sync(h.hosts)


def removeXML():
    for f in os.listdir(directory+"/"+nmap['path']):
        if f.endswith('.xml'):
            os.remove(directory+"/"+nmap['path']+"/"+f)


if __name__ == '__main__':

    initScript()

    print("------------------------")
    print("addres:" + str(netbox['address']) + "\ntoken: " + str(netbox['token']) + "\ntls_verify: " +
          str(netbox['tls_verify']) + "\ntag: " + str(nmap['tag']) + "\ncleanup: " + str(nmap.getboolean('cleanup')))
    print("------------------------")

    scanner = NetBoxScanner(
        netbox['address'],
        netbox['token'],
        netbox['tls_verify'],
        nmap['tag'],
        nmap.getboolean('cleanup')
    )

    print('Syncing...')
    cmd_nmap(scanner)

    print('Removing XML files...')
    removeXML()
