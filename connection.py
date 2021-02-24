# Bitcoin P2P network transactions analyser
#
# This file is based on https://github.com/sebicas/bitcoin-sniffer by @sebicas
#
# Distributed under the MIT/X11 software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import asyncore
import socket
import struct
import time
from StringIO import StringIO

from serializers import *

from event import Event


class Connection(asyncore.dispatcher):

    messagemap = {
        "version": msg_version,
        "verack": msg_verack,
        "addr": msg_addr,
        "alert": msg_alert,
        "inv": msg_inv,
        "getdata": msg_getdata,
        "getblocks": msg_getblocks,
        "tx": msg_tx,
        "block": msg_block,
        "getaddr": msg_getaddr,
        "ping": msg_ping

    }

    def __init__(self, host, database):
        asyncore.dispatcher.__init__(self)
        self.dstaddr = host[0]
        self.dstport = host[1]
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendbuf = ""
        self.recvbuf = ""
        self.ver_send = 209
        self.ver_recv = 209
        self.last_sent = 0
        self.state = "connecting"
        self.event = Event(database)

        vt = msg_version()
        vt.addrTo.ip = self.dstaddr
        vt.addrTo.port = self.dstport
        vt.addrFrom.ip = "0.0.0.0"
        vt.addrFrom.port = 0
        self.send_message(vt, True)
        print("\n Blockchain transactions analyzer")
        print("Connection to peer: ", self.dstaddr)
        try:
            self.connect((self.dstaddr, self.dstport))
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

    def handle_read(self):
        try:
            t = self.recv(8192)
        except:
            self.handle_close()
            return
        if len(t) == 0:
            self.handle_close()
            return
        self.recvbuf += t
        self.got_data()

    def readable(self):
        return True

    def writable(self):
        return (len(self.sendbuf) > 0)

    def handle_write(self):
        try:
            sent = self.send(self.sendbuf)
        except:
            self.handle_close()
            return
        self.sendbuf = self.sendbuf[sent:]

    def got_data(self):
        while True:

            if len(self.recvbuf) < 4:
                return

            if self.recvbuf[:4] != "\xf9\xbe\xb4\xd9":
                raise ValueError("Got garbage %s" % repr(self.recvbuf))

            if self.ver_recv < 209:
                if len(self.recvbuf) < 20:
                    return

                command = self.recvbuf[4:16].split("\x00", 1)[0]
                msglen = struct.unpack("<i", self.recvbuf[16:20])[0]
                checksum = None

                if len(self.recvbuf) < 20 + msglen:
                    return

                msg = self.recvbuf[20:20 + msglen]
                self.recvbuf = self.recvbuf[20 + msglen:]
            else:

                if len(self.recvbuf) < 24:
                    return

                command = self.recvbuf[4:16].split("\x00", 1)[0]
                msglen = struct.unpack("<i", self.recvbuf[16:20])[0]
                checksum = self.recvbuf[20:24]

                if len(self.recvbuf) < 24 + msglen:
                    return

                msg = self.recvbuf[24:24 + msglen]
                th = sha256(msg)
                h = sha256(th)

                if checksum != h[:4]:
                    raise ValueError("Bad checksum {}".format(repr(self.recvbuf)))
                self.recvbuf = self.recvbuf[24 + msglen:]

            if command in self.messagemap:
                f = StringIO(msg)
                t = self.messagemap[command]()
                t.deserialize(f)
                self.got_message(t)
            else:
                print("Unknown command {}".format(command))

    def send_message(self, message, pushbuf=False):
        if self.state != "connected" and not pushbuf:
            return
        command = message.command
        data = message.serialize()
        tmsg = "\xf9\xbe\xb4\xd9"
        tmsg += command
        tmsg += "\x00" * (12 - len(command))
        tmsg += struct.pack("<I", len(data))

        if self.ver_send >= 209:
            th = sha256(data)
            h = sha256(th)
            tmsg += h[:4]

        tmsg += data
        self.sendbuf += tmsg
        self.last_sent = time.time()

    def got_message(self, message):
        if self.last_sent + 30 * 60 < time.time():
            self.send_message(msg_ping())
        if message.command == "version":
            if message.nVersion >= 209:
                self.send_message(msg_verack())
            self.ver_send = min(MY_VERSION, message.nVersion)
            if message.nVersion < 209:
                self.ver_recv = self.ver_send
        elif message.command == "verack":
            self.ver_recv = self.ver_send
        elif message.command == "inv":
            want = msg_getdata()
            for i in message.inv:
                if i.type == 1:
                    want.inv.append(i)
                elif i.type == 2:
                    want.inv.append(i)
            if len(want.inv):
                self.send_message(want)
        elif message.command == "tx":
            self.event.new_transaction(message.tx)

        elif message.command == "block":
            self.event.new_block(message.block)
