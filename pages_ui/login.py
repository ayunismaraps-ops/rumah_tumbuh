"""Halaman login & pembuatan akun pemilik pertama."""
import streamlit as st
from app import auth


def buat_akun_pemilik(conn):
    st.title("🌱 Selamat datang di Rumah Tumbuh")
    st.subheader("Buat Akun Pemilik")
    nama = st.text_input("Nama Anda")
    username = st.text_input("Username (untuk masuk)")
    p1 = st.text_input("Password (minimal 8 karakter)", type="password")
    p2 = st.text_input("Ulangi password", type="password")
    if st.button("Buat Akun", type="primary"):
        if p1 != p2:
            st.error("Password dan ulangannya tidak sama")
        elif (e := auth.buat_user(conn, nama, username, p1, "Pemilik")):
            st.error(e)
        else:
            st.success("Akun dibuat. Silakan masuk.")
            st.rerun()


def tampil_login(conn):
    st.title("🌱 Rumah Tumbuh")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Masuk", type="primary"):
        user, pesan = auth.cek_login(conn, username, password, st.session_state)
        if user:
            st.session_state["user"] = dict(user)
            st.rerun()
        else:
            st.error(pesan)
