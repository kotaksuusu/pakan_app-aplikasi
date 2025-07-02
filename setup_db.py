# setup_db.py
from db.koneksi import get_conn

def setup():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS pakan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            jumlah INTEGER,
            harga INTEGER,
            expired TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS pemakaian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_barang TEXT,
            jumlah INTEGER,
            deskripsi TEXT,
            waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup()
