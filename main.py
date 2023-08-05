import streamlit as st
import pandas as pd
import os
from user_utils import login, register, update_profile, load_profile
from item_utils import load_items, save_items, add_item, view_items, delete_item, search_item, edit_item, export_data

# Inisialisasi state
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame(columns=['Nama Barang', 'Jumlah', 'Kategori', 'Berat (Kg)'])

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False

if 'register' not in st.session_state:
    st.session_state['register'] = False

# Menu
if not st.session_state.get('loggedin', False):
    menu = ['Login', 'Register']
else:
    menu = ['Tambah Barang', 'Lihat Barang', 'Hapus Barang', 'Profil', 'Ekspor Data', 'Riwayat Aktivitas']

choice = st.sidebar.selectbox('Menu', menu, key='menu_selectbox')

# Halaman Login
if choice == 'Login':
    st.subheader('Login ke Akun Anda')
    st.session_state['username'] = st.text_input('Username', key='login_username')
    st.session_state['password'] = st.text_input('Password', type='password', key='login_password')
    submit_button = st.button('Login', key='login_button')

    if submit_button:
        if login(st.session_state['username'], st.session_state['password']):
            st.session_state['loggedin'] = True
            st.session_state['df'] = load_items(st.session_state['username'])  # Muat item setelah login
            st.success('Berhasil login')
        else:
            st.error('Username atau password salah')

# Halaman Register
elif choice == 'Register':
    st.subheader('Buat Akun Baru')
    with st.form(key='register_form'):
        username = st.text_input('Username', key='register_username')
        password = st.text_input('Password', type='password', key='register_password')
        submit_button = st.form_submit_button('Register')
        if submit_button:
            if register(username, password):
                st.success('Berhasil membuat akun')
                st.session_state['register'] = False
            else:
                st.error('Username sudah ada')

# Halaman Tambah Barang
elif choice == 'Tambah Barang':
    st.subheader('Tambah Barang Baru')
    name = st.text_input('Nama Barang')
    quantity = st.number_input('Jumlah', value=1)
    category = st.text_input('Kategori')
    weight = st.number_input('Berat (Kg)', value=1.0)
    if st.button('Tambah'):
        if name:  # Cek jika nama barang tidak kosong
            add_item(name, quantity, category, weight)
            save_items(st.session_state['username'], st.session_state['df'])  # Simpan item setelah menambahkan barang
            st.success('Berhasil menambahkan barang')
            # Tulis ke activity.log
            with open(f'{st.session_state["username"]}_activity.log', 'a') as f:
                f.write(f"Barang {name} ditambahkan.\n")
        else:
            st.warning('Harap isi nama barang')

# Halaman Lihat Barang
elif choice == 'Lihat Barang':
    st.subheader('Daftar Barang')
    view_items()

    # Cari Barang
    st.subheader('Cari Barang')
    name = st.text_input('Nama Barang')
    if st.button('Cari'):
        result = search_item(name)
        st.write(result)
        with open('activity.log','a') as f:
            f.write(f"Barang {name} telah dicari.\n")

    # Edit Barang
    st.subheader('Edit Barang')
    if len(st.session_state['df']) > 0:
        old_name = st.selectbox('Nama Barang', st.session_state['df']['Nama Barang'].unique())
        item_df = st.session_state['df'][st.session_state['df']['Nama Barang'] == old_name]
        if len(item_df) > 0:
            new_name = st.text_input('Nama Barang Baru', value=old_name)
            quantity = st.number_input('Jumlah', value=int(item_df['Jumlah'].values[0]))
            category = st.text_input('Kategori', value=item_df['Kategori'].values[0])
            if 'Berat (Kg)' in st.session_state['df'].columns and not pd.isnull(item_df['Berat (Kg)'].values[0]):
                weight = st.number_input('Berat (Kg)', value=float(item_df['Berat (Kg)'].values[0]))
            else:
                weight = st.number_input('Berat (Kg)', value=1.0)
            if st.button('Edit'):
                edit_item(old_name, new_name, quantity, category, weight)
                st.success('Berhasil mengedit barang')
                with open('activity.log','a') as f:
                    f.write(f"Barang {old_name} telah diedit.\n")
        else:
            st.write('Tidak ada barang dengan nama tersebut')
    else:
        st.write('Tidak ada barang untuk diedit')

# Halaman Hapus Barang
elif choice == 'Hapus Barang':
    st.subheader('Hapus Barang')
    if len(st.session_state['df']) > 0:
        name = st.selectbox('Nama Barang', st.session_state['df']['Nama Barang'].unique())
        quantity = st.number_input('Jumlah', min_value=1, max_value=int(st.session_state['df'][st.session_state['df']['Nama Barang'] == name]['Jumlah'].values[0]), value=1)
        if st.button('Hapus'):
            delete_item(name, quantity)
            st.success('Berhasil menghapus barang')
            with open('activity.log','a') as f:
                f.write(f"Barang {name} telah dihapus dengan jumlah {quantity}.\n")
    else:
        st.write('Tidak ada barang untuk dihapus')

# Halaman Profil
elif choice == 'Profil':
    st.subheader('Profil Anda')
    with st.form(key='profile_form'):
        name = st.text_input('Nama')
        email = st.text_input('Email')
        address = st.text_input('Alamat')
        phone = st.text_input('No HP')
        submit_button = st.form_submit_button('Update Profil')

    if submit_button:
        if update_profile(st.session_state['username'], name, email, address, phone):
            st.success('Berhasil memperbarui profil')
        else:
            st.error('Gagal memperbarui profil')

# Halaman Ekspor Data
elif choice == 'Ekspor Data':
    st.subheader('Ekspor Data')
    export_data()

# Halaman Riwayat Aktivitas
elif choice == 'Riwayat Aktivitas':
    st.subheader('Riwayat Aktivitas')
    if not os.path.exists(f'{st.session_state["username"]}_activity.log'):
        with open(f'{st.session_state["username"]}_activity.log', 'w') as f:
            f.write('')  # Buat file kosong
    with open(f'{st.session_state["username"]}_activity.log', 'r') as f:
        st.text(f.read())
