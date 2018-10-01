import time
import struct
import random
import hashlib


from getmyip import get_my_ip


def create_message(peers, peer_index, command):

    # The current protocol version, look it up under https://bitcoin.org/en/developer-reference#protocol-versions
    version = struct.pack("i", 70015)
    services = struct.pack("Q", 0)
    timestamp = struct.pack("q", int(time.time()))
    add_recv_services = struct.pack("Q", 0)
    add_recv_ip = struct.pack(">16s", bytes(peers[peer_index][0], 'utf-8'))
    add_recv_port = struct.pack(">H", 8333)
    add_trans_services = struct.pack("Q", 0)
    add_trans_ip = struct.pack(">16s", bytes(get_my_ip(), 'utf-8'))
    add_trans_port = struct.pack(">H", 8333)
    nonce = struct.pack("Q", random.getrandbits(64))
    user_agent_bytes = struct.pack("B", 0)
    starting_height = struct.pack("i", 525453)
    relay = struct.pack("?", False)

    payload = version + services + timestamp + add_recv_services + add_recv_ip + add_recv_port + \
              add_trans_services + add_trans_ip + add_trans_port + nonce + user_agent_bytes + starting_height + relay

    magic = bytes.fromhex("F9BEB4D9")
    length = struct.pack("I", len(payload))
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]

    return magic + command + length + checksum + payload


def create_version_message(peers, peer_index):
    command = b"version" + 5 * b"\00"
    return create_message(peers, peer_index, command)


def create_addr_message(peers, peer_index):
    command = b"addr" + 5 * b"\00"
    return create_message(peers, peer_index, command)


def create_verack_message(peers, peer_index):
    command = b"verack" + 5 * b"\00"
    return create_message(peers, peer_index, command)


def create_tx_message(peers, peer_index):
    command = b"tx" + 5 * b"\00"
    return create_message(peers, peer_index, command)


def encode_received_message(recv_message):

    recv_magic = recv_message[:4].hex()
    recv_command = recv_message[4:16]
    recv_length = struct.unpack("I", recv_message[16:20])
    recv_checksum = recv_message[20:24]
    recv_payload = recv_message[24:]
    recv_version = struct.unpack("i", recv_payload[:4])

    return (recv_magic, recv_command, recv_length, recv_checksum, recv_payload, recv_version)
