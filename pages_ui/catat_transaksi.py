"""Form catat transaksi. Pengguna TIDAK memilih debit/kredit; sistem menentukannya."""
from datetime import date, datetime
import streamlit as st
from app import services, ledger, db
from app.config import PILIHAN_TUJUAN, AKUN_ASET, AKUN_BARANG
from app.money import format_rupiah

MENU = ["Pemasukan", "Pengeluaran", "Transaksi Lainnya"]


def tampil(conn, user):
    aturan = db.ambil_aturan(conn)
    edit_id = st.session_state.get("edit_id")
    lama = ledger.ambil_transaksi(conn, edit_id) if edit_id else None
    st.title("✏️ Ubah Transaksi" if lama else "➕ Catat Transaksi")
    if lama:
        st.info("Transaksi lama akan dibatalkan dan diganti dengan data baru ini.")
    if st.session_state.pop("sukses", None):
        st.success("Transaksi berhasil disimpan ✅")

    # kunci widget ikut berubah agar form kosong lagi setelah simpan
    k = f"{edit_id or 'baru'}_{st.session_state.get('form_ke', 0)}_"
    d = dict(lama) if lama else {}

    menu_awal = aturan[d["jenis_transaksi"]]["menu"] if lama else MENU[0]
    menu = st.radio("Jenis kegiatan", MENU, index=MENU.index(menu_awal), horizontal=True, key=k + "menu")
    daftar = [j for j, a in aturan.items() if a["menu"] == menu]
    idx = daftar.index(d["jenis_transaksi"]) if lama and d["jenis_transaksi"] in daftar else 0
    jenis = st.selectbox("Jenis transaksi", daftar, index=idx, key=k + "jenis")
    a = aturan[jenis]

    tanggal = st.date_input("Tanggal", value=datetime.strptime(d["tanggal"], "%Y-%m-%d").date()
                            if lama else date.today(), key=k + "tgl")

    opsi_bayar = a["pembayaran_valid"].split("|")
    if opsi_bayar == ["-"]:
        metode = "-"
    else:
        i = opsi_bayar.index(d["metode_bayar"]) if lama and d["metode_bayar"] in opsi_bayar else 0
        metode = st.selectbox("Cara bayar / terima", opsi_bayar, index=i, key=k + "metode")

    # Pilihan tambahan (hanya tampil bila dibutuhkan)
    tujuan = aset = barang = None
    if a["butuh_tujuan"]:
        tujuan = st.radio("Biaya ini untuk apa?", PILIHAN_TUJUAN, key=k + "tujuan",
                          index=PILIHAN_TUJUAN.index(d["tujuan"]) if lama and d.get("tujuan") else 0,
                          help="Operasional = biaya rutin. Tanaman Belum Menghasilkan = biaya menanam tanaman baru.")
    if a["butuh_aset"]:
        pil = list(AKUN_ASET)
        aset = st.selectbox("Aset yang disusutkan", pil, key=k + "aset",
                            index=pil.index(d["aset"]) if lama and d.get("aset") in pil else 0)
    if a["butuh_barang"]:
        pil = list(AKUN_BARANG)
        barang = st.selectbox("Barang", pil, key=k + "barang",
                              index=pil.index(d["barang"]) if lama and d.get("barang") in pil else 0)

    # Nominal: langsung, atau jumlah x harga
    cara = st.radio("Cara mengisi uang", ["Langsung isi nominal", "Jumlah × harga satuan"],
                    horizontal=True, key=k + "cara",
                    index=1 if lama and d.get("harga_satuan") else 0)
    jumlah, satuan, harga = 0.0, None, None
    if cara == "Jumlah × harga satuan":
        c1, c2, c3 = st.columns(3)
        jumlah = c1.number_input("Jumlah", min_value=0.0, step=0.5, format="%.2f",
                                 value=float(d.get("jumlah") or 0), key=k + "jml")
        satuan = c2.text_input("Satuan (kg, karung, dll.)", value=d.get("satuan") or "kg", key=k + "sat")
        harga = c3.number_input("Harga per satuan (Rp)", min_value=0, step=1000,
                                value=int(d.get("harga_satuan") or 0), key=k + "hrg")
        nominal = round(jumlah * harga)
        st.write(f"Total: **{format_rupiah(nominal)}**")
    else:
        nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000,
                                  value=int(d.get("nominal") or 0), key=k + "nom")
        if a["jenis_transaksi"] in ("Jual Hasil Pengepulan", "Beli Hasil Pengepulan") or (
                jenis == "Kerugian Persediaan" and barang == "Hasil Pengepulan"):
            jumlah = st.number_input("Jumlah barang (kg)", min_value=0.0, step=0.5, format="%.2f",
                                     value=float(d.get("jumlah") or 0), key=k + "jml2")
            satuan = "kg"

    keterangan = st.text_input("Keterangan (wajib)", value=d.get("keterangan") or "", key=k + "ket")
    with st.expander("Data tambahan (boleh dikosongkan)"):
        pihak = st.text_input("Nama pemasok / pelanggan", value=d.get("pihak") or "", key=k + "pihak")
        invoice = st.text_input("Nomor invoice", value=d.get("no_invoice") or "", key=k + "inv")
        blok = st.text_input("Blok / lahan", value=d.get("blok_lahan") or "", key=k + "blok")
        catatan = st.text_area("Catatan", value=d.get("catatan") or "", key=k + "cat")

    data = dict(tanggal=tanggal, jenis_transaksi=jenis, metode=metode, keterangan=keterangan,
                jumlah=jumlah, satuan=satuan, harga_satuan=harga, nominal=nominal, pihak=pihak or None,
                no_invoice=invoice or None, blok_lahan=blok or None, catatan=catatan or None,
                tujuan=tujuan, aset=aset, barang=barang)

    konfirmasi = st.session_state.get("stok_kurang") == k
    if konfirmasi:
        st.warning("Stok hasil pengepulan tidak cukup. Nilai HPP dihitung dari stok yang ada.")
        konfirmasi = st.checkbox("Saya mengerti, tetap simpan", key=k + "ok")

    if st.button("💾 Simpan", type="primary", key=k + "simpan"):
        try:
            services.simpan_transaksi(conn, data, user["id"], konfirmasi_stok=konfirmasi, ganti_id=edit_id)
            st.session_state.pop("stok_kurang", None)
            st.session_state.pop("edit_id", None)
            st.session_state["form_ke"] = st.session_state.get("form_ke", 0) + 1
            st.session_state["sukses"] = True
            st.rerun()
        except services.ValidasiError as e:
            for pesan in e.errors:
                st.error(pesan)
        except services.StokKurang as e:
            st.session_state["stok_kurang"] = k
            st.warning(f"Stok tersedia hanya {e.tersedia:g}, Anda menjual {e.diminta:g}. "
                       "Centang konfirmasi lalu simpan lagi.")
        except Exception as e:
            st.error(f"Gagal menyimpan: {e}")
    if lama and st.button("Batal ubah"):
        st.session_state.pop("edit_id")
        st.rerun()
