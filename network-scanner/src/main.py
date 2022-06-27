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


import paramiko
import json
import paramiko
import os
import sys
import pyfiglet
import time

from paramiko import SSHException
from data.data import Data

directory = os.path.dirname(sys.argv[0])
path = directory+'/secret.json'

# CPD Orange
network_orange = directory+"/network-orange.json"

# CPD Campus
network_campus = directory+"/network-campus.json"


def read_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return Data(data['hostname'], data['username'], data['password'])


def read_network(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        # print(data["DMZC"]["ip"])
        return data


def ssh_connect(data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(data.hostname, username=data.username,
                    password=data.password)
        print('Successfully connected to {}'.format(data.hostname))
        return ssh
    except SSHException:
        print('Connection failed')
        ssh.close()
        exit()


def execute_command(sshConnection, ip, host):
    MAGIC_NUMBER = 10

    try:

        print("Executing command on {}".format(ip))

        # Execute command on client
        stdin, stdout, stderr = sshConnection.exec_command(
            "zabbix_get -s "+host+" -k system.run['sudo nmap -PR -F '"+ip+"'/24 -oX /tmp/nmap.xml']", timeout=100)

        lineas = 0
        aux = ""
        print("Getting output from {}".format(ip))

        # Wait for command to finish
        time.sleep(10)

        # Read output
        stdin, stdout, stderr = sshConnection.exec_command(
            "zabbix_get -s "+host+" -k system.run['cat /tmp/nmap.xml']")

        aux = stdout.read().decode('utf-8')
        lineas = aux.count('\n')

        if lineas < MAGIC_NUMBER:
            print("No host found on {}".format(ip))
            exit(-1)

        # Remove file from server
        stdin, stdout, stderr = sshConnection.exec_command(
            "zabbix_get -s "+host+" -k system.run['rm /tmp/nmap.xml']")

        print("Data from {}".format(host))
        return aux

    except SSHException:
        print("Error: Connection to {} failed".format(host))


def write_xml(data, network):

    # Write output to file
    with open(directory+"/nmap-"+network+"-24.xml", 'w') as f:
        f.write(data)
        f.close()


if __name__ == '__main__':

    print(pyfiglet.figlet_format('Netbox - Scanner by David Marquet', width=200))

    # Read data from path 'secret.json'
    environment = read_file(path)

    try:

        # Connect to server
        sshConnection = ssh_connect(environment)

        # Load data from network-orange.json
        network_orange = read_network(network_orange)

        for network in network_orange:
            # Execute command on client
            data = execute_command(
                sshConnection, network_orange[network]["network"], network_orange[network]["ip"])

            # Write output to file
            write_xml(data, network_orange[network]["network"])

        # Load data from network-campus.json
        network_campus = read_network(network_campus)

        for network in network_campus:
            # Execute command on client
            data = execute_command(
                sshConnection, network_campus[network]["network"], network_campus[network]["ip"])

            # Write output to file
            write_xml(data, network_campus[network]["network"])

    except SSHException:
        print("Error: Connection to {} failed".format(environment.hostname))

    # Close connection
    sshConnection.close()
