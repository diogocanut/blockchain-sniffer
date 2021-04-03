
# Bitcoin P2P network transactions analyser
#
# This project is a fork of https://github.com/sebicas/bitcoin-sniffer by @sebicas
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import asyncore
import socket

from connection import Connection

from database import DatabaseInterface


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_node_addresses():

    dns_seeds = [
        ("seed.bitcoin.sipa.be", 8333),
        ("dnsseed.bluematt.me", 8333),
        ("dnsseed.bitcoin.dashjr.org", 8333),
        ("seed.bitcoinstats.com", 8333),
        # ("seed.bitnodes.io", 8333),
    ]

    found_peers = []
    try:

        for (ip_address, port) in dns_seeds:
            for info in socket.getaddrinfo(ip_address, port,
                                           socket.AF_INET, socket.SOCK_STREAM,
                                           socket.IPPROTO_TCP):
                found_peers.append((info[4][0], info[4][1]))
        return found_peers
    except Exception as e:
        print('Invalid dns seed {}'.format(e))
        raise

if __name__ == '__main__':
    hosts = get_node_addresses()

    database = DatabaseInterface()

    maxConnections = 2

    if hosts is None:
        raise IndexError('Hosts is None')

    for host in hosts:
        c = Connection(host, database)

    asyncore.loop()

    database.close()
