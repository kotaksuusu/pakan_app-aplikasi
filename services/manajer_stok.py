# services/manajer_stok.py
from models.pakan import Pakan
from models.pemakaian import Pemakaian
from db.koneksi import get_conn
import sqlite3

class ManajerStok:
    def __init__(self):
        self.conn = get_conn()
        self.cursor = self.conn.cursor()

    def tambah_pakan(self, pakan: Pakan):
        self.cursor.execute("""
            INSERT INTO pakan (nama, jumlah, harga, expired)
            VALUES (?, ?, ?, ?)""",
            (pakan.nama, pakan.jumlah, pakan.harga, pakan.expired))
        self.conn.commit()

    def get_stok_tersedia(self):
        return self.cursor.execute("SELECT * FROM pakan WHERE jumlah > 0").fetchall()

    def catat_pemakaian(self, pemakaian: Pemakaian):
        stok = self.cursor.execute("SELECT jumlah FROM pakan WHERE nama = ?", (pemakaian.nama_barang,)).fetchone()
        if stok:
            jumlah_sekarang = stok["jumlah"]
            if pemakaian.jumlah > jumlah_sekarang:
                return False
            sisa = jumlah_sekarang - pemakaian.jumlah
            if sisa == 0:
                self.cursor.execute("DELETE FROM pakan WHERE nama = ?", (pemakaian.nama_barang,))
            else:
                self.cursor.execute("UPDATE pakan SET jumlah = ? WHERE nama = ?", (sisa, pemakaian.nama_barang))
            self.cursor.execute("""
                INSERT INTO pemakaian (nama_barang, jumlah, deskripsi)
                VALUES (?, ?, ?)""",
                (pemakaian.nama_barang, pemakaian.jumlah, pemakaian.deskripsi))
            self.conn.commit()
            return True
        return False

    def get_riwayat_pemakaian(self):
        return self.cursor.execute("SELECT * FROM pemakaian ORDER BY waktu DESC").fetchall()

    def get_semua_stok(self):
        return self.cursor.execute("SELECT * FROM pakan").fetchall()

    def hapus_pakan(self, id_pakan: int):
        self.cursor.execute("DELETE FROM pakan WHERE id = ?", (id_pakan,))
        self.conn.commit()
