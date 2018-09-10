import socket
import time
import struct
import random
import hashlib

from getaddresses import get_node_addresses

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect(peer_index):
    try:
        print("Trying to connect to ", peers[peer_index])
        err = sock.connect(peers[peer_index])
        return peer_index
    except Exception:
        return connect(peer_index+1)

peer_index = connect(0)

def create_version_message():

    # The current protocol version, look it up under https://bitcoin.org/en/developer-reference#protocol-versions
    version = struct.pack("i", 70015)
    services = struct.pack("Q", 0)
    timestamp = struct.pack("q", int(time.time()))
    add_recv_services = struct.pack("Q", 0)
    add_recv_ip = struct.pack(">16s", bytes(peers[peer_index][0], 'utf-8'))
    add_recv_port = struct.pack(">H", 8333)
    add_trans_services = struct.pack("Q", 0)
    add_trans_ip = struct.pack(">16s", bytes("127.0.0.1", 'utf-8'))
    add_trans_port = struct.pack(">H", 8333)
    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent_bytes = struct.pack("B", 0)
    starting_height = struct.pack("i", 525453)
    relay = struct.pack("?", False)

    payload = version + services + timestamp + add_recv_services + add_recv_ip + add_recv_port + \
              add_trans_services + add_trans_ip + add_trans_port + nonce + user_agent_bytes + starting_height + relay

    magic = bytes.fromhex("F9BEB4D9")
    command = b"version" + 5 * b"\00"
    length = struct.pack("I", len(payload))
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

    return magic + command + length + checksum + payload

