import psycopg2
from psycopg2 import sql
import pandas_datareader as data

def connect():
    cons = "dbname='transactions' user='postgres' host='localhost' port='5433' password='postgres'"
    try:
        conn = psycopg2.connect(cons)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

def create_tables(conn, cur):
    """ create tables in the PostgreSQL database"""
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
                op_codes TEXT NOT NULL,
                PRIMARY KEY (transaction_hash, script_pub_key),
                FOREIGN KEY (transaction_hash)
                    REFERENCES transactions (hash)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    try:
        for command in commands:
            cur.execute(command)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def start_db():
    conn = connect()
    cur = conn.cursor()
    create_tables(conn, cur)
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()



