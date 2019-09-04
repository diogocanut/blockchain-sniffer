import binascii
from parser import *


class Event(object):

    def __init__(self):
        self.parser = Parser()
        self.transactions = {}

    def new_block(block):
        if block.is_valid(self):
            print("\n - Valid Block: %s") % block.hash
        else:
            print("\n - Invalid Block: %s") % block.hash


    def new_transaction(self, tx, file):
        if tx.is_valid():
            print("\n - Valid TX: %s\n") % tx.hash
            if tx.hash not in self.transactions:
                self.transactions[tx.hash] = tx
                # TODO: CHANGE THE FILE TO DATABASE
                file.write("hash: {}\n\t{}\n\n".format(tx.hash, tx))
                file.flush()
            for txout in tx.vout:
                print("     To: %s BTC: %.8f" % (txout.address, txout.amount))
                script = binascii.hexlify(txout.scriptPubKey)
                self.parser.get_script(script)
        else:
            print("\n - Invalid TX: %s" % tx.hash)