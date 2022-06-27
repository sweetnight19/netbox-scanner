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

import unittest
from os import environ
from nbs.nmap import Nmap


class TestRequest(unittest.TestCase):
    def test_api(self):
        path = environ.get('../netbox-scanner.conf')

        nmap = Nmap(path, 'test')
        self.assertIsInstance(nmap, Nmap)
        nmap.run()
        self.assertIsInstance(nmap.hosts, list)


if __name__ == '__main__':
    unittest.main()
