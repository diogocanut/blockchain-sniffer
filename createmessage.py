import time
import struct
import random
import hashlib
import socket


from getmyip import get_my_ip

MY_VERSION = 70015


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


def encode_addr_message(recv_message):

    recv_time = recv_message[:4]
    recv_services = recv_message[4:12]
    recv_ip = recv_message[12:28]
    recv_port = recv_message[:2]

    return (
        recv_time,
        recv_services,
        recv_ip,
        recv_port,
    )


class CAddress(object):
    def __init__(self):
        self.nServices = 1
        self.pchReserved = "\x00" * 10 + "\xff" * 2
        self.ip = "0.0.0.0"
        self.port = 0

    def deserialize(self, f):
        self.nServices = struct.unpack("<Q", f.read(8))[0]
        self.pchReserved = f.read(12)
        self.ip = socket.inet_ntoa(f.read(4))
        self.port = struct.unpack(">H", f.read(2))[0]

    def serialize(self):
        nServices = struct.pack("<Q", self.nServices)
        pchReserved = self.pchReserved
        ip = socket.inet_aton(self.ip)
        port = struct.pack(">H", self.port)
        return (nServices, pchReserved, ip, port)

    def __repr__(self):
        return "CAddress(nServices=%i ip=%s port=%i)" % (self.nServices, self.ip, self.port)


class msg_version(object):
    command = "version"

    def __init__(self):
        self.nVersion = MY_VERSION
        self.nServices = 1
        self.nTime = int(time.time())
        self.addrTo = CAddress()
        self.addrFrom = CAddress()
        self.nNonce = random.getrandbits(64)
        self.nStartingHeight = -1

    def deserialize(self, f):
        self.nVersion = struct.unpack("<i", f.read(4))[0]
        if self.nVersion == 10300:
            self.nVersion = 300
        self.nServices = struct.unpack("<Q", f.read(8))[0]
        self.nTime = struct.unpack("<q", f.read(8))[0]
        self.addrTo = CAddress()
        self.addrTo.deserialize(f)
        if self.nVersion >= 106:
            self.addrFrom = CAddress()
            self.addrFrom.deserialize(f)
            self.nNonce = struct.unpack("<Q", f.read(8))[0]
            if self.nVersion >= 209:
                self.nStartingHeight = struct.unpack("<i", f.read(4))[0]
            else:
                self.nStartingHeight = None
        else:
            self.addrFrom = None
            self.nNonce = None
            self.nStartingHeight = None

    def serialize(self):
        nVersion = struct.pack("<i", self.nVersion)
        nServices = struct.pack("<Q", self.nServices)
        nTime = struct.pack("<q", self.nTime)
        addrTo = self.addrTo.serialize()
        addrFrom = self.addrFrom.serialize()
        nNonce = struct.pack("<Q", self.nNonce)
        nStartingHeight = struct.pack("<i", self.nStartingHeight)
        return nVersion + nServices + nTime + addrTo + addrFrom + nNonce + nStartingHeight
