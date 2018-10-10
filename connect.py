import asyncore, socket
import time
import struct

from createmessage import (
    create_version_message,
    encode_received_message,
    encode_addr_message,
    create_addr_message,
    create_verack_message,
    create_tx_message,
    msg_version,
    )
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

    # Worked on 108.170.45.186

    peers = get_node_addresses()
    peer_index = connect_peers(peers, 0)

    time.sleep(1)
    print("Connected to: ", peers[peer_index][0])
    sock.send(create_version_message(peers, peer_index))

    version = encode_received_message(sock.recv(166))
    print(version[-1])

    sock.send(create_verack_message(peers, peer_index))
    # verack2 = sock.recv(80)
    # print(verack2)

    sock.send(create_addr_message(peers, peer_index))
    msg = encode_addr_message(sock.recv(8192))
    print(msg)


class NodeConn(asyncore.dispatcher):

    def __init__(self, dstaddr, dstport):
        asyncore.dispatcher.__init__(self)
        self.dstaddr = dstaddr
        self.dstport = dstport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendbuf = ""
        self.recvbuf = ""
        self.ver_send = 209
        self.ver_recv = 209
        self.last_sent = 0
        self.state = "connecting"

        version_message = msg_version()
        self.send_message(version_message, True)
        print("\n Blockchain transactions analyzer")
        print("Connection to peer: ", self.dstaddr)
        try:
            self.connect((dstaddr, dstport))
        except:
            self.handle_close()

    def handle_connect(self):
        print("Connection realized\n")
        self.state = "connected"

    def handle_close(self):
        print("Ending connection")
        self.state = "closed"
        self.recvbuf = ""
        self.sendbuf = ""
        try:
            self.close()
        except:
            pass

    def send_message(self, message, pushbuf=False):
        if self.state != "connected" and not pushbuf:
            return
        print(message)
        command = message.command
        data = message.serialize()
        tmsg = "\xf9\xbe\xb4\xd9"
        tmsg += command
        tmsg += "\x00" * (12 - len(command))
        tmsg += str(struct.pack("<I", len(data)))
        # if self.ver_send >= 209:
        #     th = sha256(data)
        #     h = sha256(th)
        #     tmsg += h[:4]
        tmsg += str(data)
        msg2 = create_version_message(('108.170.45.186', 8333), 0)
        print(msg2)
        print(tmsg)
        self.sendbuf += tmsg
        self.last_sent = time.time()


if __name__ == '__main__':
    c = NodeConn('108.170.45.186', 8333)
    asyncore.loop()
