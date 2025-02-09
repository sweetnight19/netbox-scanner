#!/usr/bin/env python3

##################################################
# Author:  José Lopes (Iopes)
# Copyright: Copyright 2022, Netbox-Scanner
# License: MIT
# Version: 1.0.0
# Maintainer: David Marquet
# Email: david.marquet@salle.url.edu
# Status: Development
##################################################

import logging
import requests

from pynetbox import api


class NetBoxScanner(object):

    def __init__(self, address, token, tls_verify, tag, cleanup):
        if (tls_verify == 'no'):
            session = requests.Session()
            session.verify = False
            self.netbox = api(
                url=address, token=token)
            self.netbox.http_session = session
            self.tag = tag
            self.cleanup = cleanup
            self.stats = {
                'unchanged': 0,
                'created': 0,
                'updated': 0,
                'deleted': 0,
                'errors': 0
            }
        else:
            self.netbox = api(address, token)
            self.tag = tag
            self.cleanup = cleanup
            self.stats = {
                'unchanged': 0,
                'created': 0,
                'updated': 0,
                'deleted': 0,
                'errors': 0
            }

    def sync_host(self, host):
        '''Syncs a single host to NetBox

        host: a tuple like ('10.0.0.1','Gateway')
        returns: True if syncing is good or False for errors
        '''
        try:    # try to get host from NetBox
            nbhost = self.netbox.ipam.ip_addresses.get(address=host[0])

        except ValueError:
            logging.error(f'duplicated: {host[0]}/24')
            self.stats['errors'] += 1
            return False

        if nbhost:  # host exists
            if (self.tag in nbhost.tags):   # host has tag
                if (host[1] != nbhost.description):  # host description changed
                    aux = nbhost.description
                    nbhost.description = host[1]
                    nbhost.dns_name = "172.16.205.5"
                    nbhost.status = "active"
                    nbhost.save()
                    logging.info(
                        f'updated: {host[0]} "{aux}" -> "{host[1]}"')
                    self.stats['updated'] += 1
                else:   # host description unchanged
                    logging.info(
                        f'unchanged desciption: {host[0]} "{host[1]}"')
                    nbhost.status = "active"
                    nbhost.save()
                    self.stats['unchanged'] += 1
            else:   # host has no tag
                nbhost.status = "active"
                nbhost.save()

                logging.info(f'unchanged tag: {host[0]} "{host[1]}"')
                self.stats['unchanged'] += 1
        else:   # host does not exist
            self.netbox.ipam.ip_addresses.create(
                address=host[0],
                tags=[{"name": self.tag}],
                dns_name="172.16.205.5",
                description=host[1]
            )
            logging.info(f'created: {host[0]} "{host[1]}"')
            self.stats['created'] += 1

        return True

    def garbage_collector(self, hosts):
        '''Removes records from NetBox not found in last sync'''
        nbhosts = self.netbox.ipam.ip_addresses.filter(
            tag=self.tag)    # get all hosts with tag

        for nbhost in nbhosts:  # for each host in NetBox
            nbh = str(nbhost).split('/')[0]
            if not any(nbh == addr[0] for addr in hosts):   # host not found
                # nbhost.delete()
                #logging.info(f'deleted: {nbhost}')
                #self.stats['deleted'] += 1
                aux = nbhost.description
                nbhost.status = "deprecated"
                nbhost.dns_name = "172.16.205.5"
                nbhost.save()
                logging.info(
                    f'updated: {nbhost[0]} "{aux}" -> "{nbhost[1]}"')
                self.stats['updated'] += 1

    def sync(self, hosts):
        '''Syncs hosts to NetBox
        hosts: list of tuples like [(addr,description),...]
        '''
        for s in self.stats:    # reset stats
            self.stats[s] = 0

        logging.info('started: {} hosts'.format(len(hosts)))

        for host in hosts:  # for each host
            self.sync_host(host)    # sync host to NetBox

        if self.cleanup:    # if cleanup is enabled
            self.garbage_collector(hosts)   # remove old hosts

        logging.info('finished: .{} +{} ~{} -{} !{}'.format(
            self.stats['unchanged'],
            self.stats['created'],
            self.stats['updated'],
            self.stats['deleted'],
            self.stats['errors']
        ))

        return True
