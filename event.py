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

                self.database.insert_transaction(tx)

            for txout in tx.vout:
                print("     To: %s BTC: %.8f" % (txout.address, txout.amount))
                opcodes = self.parser.parse(txout.script())
                self.database.insert_ctxout(tx, txout, opcodes)
            for txin in tx.vin:
                self.database.insert_ctxin(tx, txin)

            self.database.conn.commit()
        else:
            print("\n - Invalid TX: %s" % tx.hash)
