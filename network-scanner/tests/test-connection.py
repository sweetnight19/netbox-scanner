import os
import sys
import json
import paramiko
from data.data import Data

directory = os.path.dirname(sys.argv[0])
path = directory+'../src/secret.json'


def readFile(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        return Data(data['hostname'], data['username'], data['password'])


def sshConnect(data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(data.hostname, username=data.username,
                    password=data.password)
        print('Successfully connected to {}'.format(data.hostname))
    except:
        print('Connection failed')

    ssh.close()


if __name__ == '__main__':
    # Read data from path 'secret.json'
    environment = readFile(path)

    # Connect to server
    sshConnection = sshConnect(environment)
