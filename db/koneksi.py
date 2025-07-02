# db/koneksi.py
import sqlite3

def get_conn():
    conn = sqlite3.connect("pakan.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
