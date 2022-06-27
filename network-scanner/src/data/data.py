#!/usr/bin python3

##################################################
# Author:  David Marquet
# Copyright: Copyright 2022, TFG-David Marquet
# License: MIT
# Version: 1.0.0
# Maintainer: David Marquet
# Email: david.marquet@salle.url.edu
# Status: Development
##################################################

class Data:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password


class Host:
    def __init__(self, name, description, type, network, machine, ip):
        self.name = name
        self.description = description
        self.type = type
        self.network = network
        self.machine = machine
        self.ip = ip
