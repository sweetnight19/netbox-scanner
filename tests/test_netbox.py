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
from nbs import NetBoxScanner


class TestRequest(unittest.TestCase):
    def test_api(self):
        #address = environ.get('172.16.205.130')
        #token = environ.get('6d922c1b19a4c4cc7bf8f9f20b0fdab6e6e885e9')

        #netbox = NetBoxScanner(address, token, False, 'test', False)
        netbox = NetBoxScanner(
            "https://netbox.salleurl.edu/", "456d132a8da430f41d62bc8991385d690b729694", False, 'test', False)
        self.assertIsInstance(netbox, NetBoxScanner)
        self.assertEqual(netbox.sync([]), True)


if __name__ == '__main__':
    unittest.main()
