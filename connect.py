import socket
import time
import codecs

from createmessage import create_version_message, encode_received_message
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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


def connect_peers(peers, peer_index):
    for p in range(peer_index, len(peers)):
        try:
            print("Trying to connect to ", peers[p])
            err = sock.connect(peers[p])
            return p
        except Exception:
            pass


def connect_ip(ip):
    try:
        err = socket.connect(ip)
        return ip
    except Exception:
        pass


def make_connection():
    peers = get_node_addresses()

    peer_index = connect_peers(peers, 2)
    time.sleep(1)
    sock.send(create_version_message(peers, peer_index))


def message():
    encoded_values = encode_received_message(sock.recv(8192))
    print("Version: ", encoded_values[-1])


if __name__ == '__main__':
    make_connection()
    message()