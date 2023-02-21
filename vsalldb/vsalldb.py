import sqlite3
import atexit
import traceback
import logging

conn = None
sqldeploytables = "CREATE TABLE IF NOT EXISTS GAMES_CRPS (ID INTEGER PRIMARY KEY AUTOINCREMENT, PLAYER1 INTEGER, PLAYER2 INTEGER, PLAYER1_CHOICE TEXT, PLAYER2_CHOICE TEXT, RESULT TEXT, PLAYED_ON DEFAULT CURRENT_TIMESTAMP)"

def get_connection():
    global conn
    if not conn:
        conn = sqlite3.connect('vsall.sqlite')
        # conn.execute(sqldeploytables) # only really needed once
    atexit.register(close_connection, conn)
    return conn

def close_connection(some_conn):
    try:
        some_conn.commit()
        some_conn.close()
    except Exception as e:
        logging.error(traceback.format_exc())