import psycopg2


class DatabaseInterface:
    # a database named transactions should be created before running
    def __connect(self):
        cons = "dbname='transactions' user='postgres' host='localhost' port='5433' password='postgres'"
        try:
            self.conn = psycopg2.connect(cons)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise

    def __initial_schema(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS transactions (
                hash TEXT PRIMARY KEY NOT NULL,
                n_version INTEGER NOT NULL,
                lock_time INTEGER NOT NULL
            )
            """,

            """
            CREATE TABLE IF NOT EXISTS CTxIns (
                    transaction_hash TEXT NOT NULL,
                    prevout UUID NOT NULL,
                    prevout_n INTEGER NOT NULL,
                    script_sig TEXT NOT NULL,
                    n_sequence BIGINT NOT NULL,
                    PRIMARY KEY (transaction_hash, script_sig),
                    FOREIGN KEY (transaction_hash)
                        REFERENCES transactions (hash)
                        ON UPDATE CASCADE ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS CTxOuts (
                    transaction_hash TEXT NOT NULL,
                    script_pub_key TEXT NOT NULL,
                    n_value DECIMAL NOT NULL,
                    op_codes TEXT[] NOT NULL,
                    amount DECIMAL NOT NULL,
                    address TEXT NOT NULL,
                    PRIMARY KEY (transaction_hash, script_pub_key),
                    FOREIGN KEY (transaction_hash)
                        REFERENCES transactions (hash)
                        ON UPDATE CASCADE ON DELETE CASCADE
            )
            """)
        try:
            for command in commands:
                self.cur.execute(command)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise

    def __init__(self):
        self.__connect()
        self.cur = self.conn.cursor()
        self.__initial_schema()

    def insert_transaction(self, tx):
        self.cur.execute(
            """INSERT INTO transactions (hash, n_version, lock_time)
            VALUES (%s, %s, %s) ON CONFLICT DO NOTHING""", (tx.hash, tx.nVersion, tx.nLockTime))

    def insert_ctxout(self, tx, ctxout, opcodes):
        script = ctxout.script()
        self.cur.execute(
            """INSERT INTO  CTxOuts (transaction_hash, script_pub_key, n_value,
            op_codes, amount, address) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (tx.hash, script, ctxout.nValue, opcodes, ctxout.amount, ctxout.address))

    def insert_ctxin(self, tx, ctxin):
        # self.cur.execute("""INSERT INTO CTxIns (transaction_hash, prevout,
        #     prevout_n, script_sig, n_sequence)
        #     VALUES (%s, %s, %s)""", (tx.hash, tx.nVersion, tx.nLockTime))
        pass

    def close(self):
        self.cur.close()
        self.conn.close()
