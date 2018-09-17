import socket
import time

from createmessage import create_version_message, encode_received_message


def get_node_addresses():

    dns_seeds = [
        ("seed.bitcoin.sipa.be", 8333),
        ("dnsseed.bluematt.me", 8333),
        ("dnsseed.bitcoin.dashjr.org", 8333),
        ("seed.bitcoinstats.com", 8333),
        ("seed.bitnodes.io", 8333),
        ("bitseed.xf2.org", 8333),
    ]

    found_peers = []
    try:

        for (ip_address, port) in dns_seeds:

            for info in socket.getaddrinfo(ip_address, port,
                                           socket.AF_INET, socket.SOCK_STREAM,
                                           socket.IPPROTO_TCP):

                found_peers.append((info[4][0], info[4][1]))
        return found_peers
    except Exception:
        return None


def connect(peers, peer_index, sock):
    try:
        print("Trying to connect to ", peers[peer_index])
        err = sock.connect(peers[peer_index])
        return peer_index
    except Exception:
        return connect(peers, peer_index+1, sock)


def make_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peers = get_node_addresses()
    if peers is not None:
        peer_index = connect(peers, 2, sock)
        sock.send(create_version_message(peers, peer_index))
        time.sleep(1)

        encoded_values = encode_received_message(sock.recv(8192))
        y = sock.recv(1000)
        print("Version: ", encoded_values[-1])
        print(y)
    else:
        print("No peer founded")
