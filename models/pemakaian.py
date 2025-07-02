# models/pemakaian.py
class Pemakaian:
    def __init__(self, nama_barang: str, jumlah: int, deskripsi: str):
        self.nama_barang = nama_barang
        self.jumlah = jumlah
        self.deskripsi = deskripsi
