# main_app.py
import streamlit as st
import pandas as pd
from models.pakan import Pakan
from models.pemakaian import Pemakaian
from services.manajer_stok import ManajerStok

st.set_page_config(page_title="Pakan Ternak OOP", layout="centered")
st.title("🐄 Manajemen Pakan Ternak")
manager = ManajerStok()

menu = st.sidebar.radio("Pilih Menu", ["Tambah Pakan", "Pemakaian", "Lihat Stok"])

if menu == "Tambah Pakan":
    st.header("➕ Tambah Pakan Baru")
    nama = st.text_input("Nama Barang")
    jumlah = st.number_input("Jumlah", min_value=1, step=1)
    harga = st.number_input("Harga Satuan", min_value=0, step=100)
    expired = st.date_input("Tanggal Expired")

    if st.button("Simpan"):
        pakan = Pakan(nama, jumlah, harga, expired.strftime("%Y-%m-%d"))
        manager.tambah_pakan(pakan)
        st.success("✅ Pakan berhasil ditambahkan.")

elif menu == "Pemakaian":
    st.header("📉 Catat Pemakaian")
    stok = manager.get_stok_tersedia()
    if stok:
        pilihan = [row['nama'] for row in stok]
        nama = st.selectbox("Nama Barang", pilihan)
        jumlah = st.number_input("Jumlah Pakai", min_value=1, step=1)
        deskripsi = st.text_area("Deskripsi")

        if st.button("Catat"):
            pemakaian = Pemakaian(nama, jumlah, deskripsi)
            if manager.catat_pemakaian(pemakaian):
                st.success("✅ Pemakaian dicatat.")
            else:
                st.warning("Jumlah melebihi stok atau tidak valid.")
    else:
        st.info("Tidak ada stok tersedia.")

elif menu == "Lihat Stok":
    st.header("📊 Data Stok Pakan")
    data = manager.get_semua_stok()
    if data:
        df = pd.DataFrame([dict(row) for row in data])
        for i, row in df.iterrows():
            with st.expander(f"{row['nama']} - Jumlah: {row['jumlah']}"):
                st.write(f"Harga: {row['harga']}")
                st.write(f"Expired: {row['expired']}")
                if st.button(f"❌ Hapus", key=f"hapus_{row['id']}"):
                    manager.hapus_pakan(row['id'])
                    st.success("Data berhasil dihapus. Silakan reload halaman.")
                    st.stop()
    else:
        st.warning("Belum ada stok pakan.")

    st.subheader("🧾 Riwayat Pemakaian")
    log = manager.get_riwayat_pemakaian()
    if log:
        df_log = pd.DataFrame([dict(row) for row in log])
        st.dataframe(df_log)
    else:
        st.info("Belum ada pemakaian tercatat.")
