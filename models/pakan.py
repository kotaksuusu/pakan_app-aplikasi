# models/pakan.py
class Pakan:
    def __init__(self, nama: str, jumlah: int, harga: int, expired: str):
        self.nama = nama
        self.jumlah = jumlah
        self.harga = harga
        self.expired = expired
