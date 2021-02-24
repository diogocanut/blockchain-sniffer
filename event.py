import binascii
from parser import Parser


class Event(object):

    def __init__(self, database):
        self.parser = Parser()
        self.transactions = {}
        self.database = database

    def new_block(self, block):
        if block.is_valid():
            print("\n - Valid Block: %s") % block.hash
        else:
            print("\n - Invalid Block: %s") % block.hash

    def new_transaction(self, tx):
        if tx.is_valid():
            print("\n - Valid TX: %s\n") % tx.hash
            if tx.hash not in self.transactions:
                self.transactions[tx.hash] = tx
                # TODO: CHANGE THE FILE TO DATABASE
                # file.write("hash: {}\n\t{}\n\n".format(tx.hash, tx))
                # file.flush()
                self.database.cur.execute("INSERT INTO transactions (hash, n_version, lock_time) VALUES (%s, %s, %s)", (tx.hash, tx.nVersion, tx.nLockTime))
            for txout in tx.vout:
                print("     To: %s BTC: %.8f" % (txout.address, txout.amount))
                script = binascii.hexlify(txout.scriptPubKey)
                self.parser.get_script(script)
                # self.cur.execute("INSERT INTO ctxouts (transaction_hash, script_pub_key, n_value) VALUES (%s, %s, %s)",
                #     (tx.hash, script, tx.nValue))
            self.database.conn.commit()
        else:
            print("\n - Invalid TX: %s" % tx.hash)
