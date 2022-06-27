#!/bin/bash

echo "Running the application"
#figlet -w 200 Netbox - Scanner by David Marquet

#get the current directory
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#echo "Current directory: $DIR"

#set up the environment
source $DIR/venv/bin/activate

echo "Scanning networks..."
python3 $DIR/network-scanner/src/main.py
echo "Done!"

#logs = $(bash nmap-scan.sh)
#echo $(bash nmap-scan.sh) >../log.txt

echo "Running netbox-scanner..."
python3 $DIR/netbox-scanner.py
echo "Done!"

#echo "Running netbox-scanner-report..."
#tar -czvf scans/nmap-"$TODAY".tar.gz *.xml

#echo "Removing XML files..."
#rm -rf *.xml

#get out of the virtual environment
deactivate
