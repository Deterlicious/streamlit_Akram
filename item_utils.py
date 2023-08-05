import pandas as pd
import streamlit as st
from datetime import date

def load_items(user):
    try:
        with open(f'{user}_items.json', 'r') as f:
            items = pd.read_json(f)
    except FileNotFoundError:
        items = pd.DataFrame(columns=['Nama Barang', 'Jumlah', 'Kategori', 'Berat (Kg)', 'Tanggal Pengembalian'])
    return items

def save_items(user, items):
    with open(f'{user}_items.json', 'w') as f:
        items.to_json(f)

def add_item(name, quantity, category, weight, return_date):
    if not name or not category:
        st.warning('Nama barang dan kategori tidak boleh kosong')
        return
    if quantity <= 0 or weight <= 0:
        st.warning('Jumlah dan berat harus lebih besar dari 0')
        return
    if return_date < date.today():
        st.warning('Tanggal pengembalian tidak boleh lebih awal dari hari ini')
        return
    new_row = pd.DataFrame({
        'Nama Barang': [name],
        'Jumlah': [quantity],
        'Kategori': [category],
        'Berat (Kg)': [weight],
        'Tanggal Pengembalian': [return_date]
    })
    st.session_state['df'] = pd.concat([st.session_state['df'], new_row], ignore_index=True)
    st.session_state['df'].index = st.session_state['df'].index + 1  # Mengubah indeks dari 0 menjadi 1
    save_items(st.session_state['username'], st.session_state['df'])  # Simpan item setelah menambahkan barang
    st.success('Berhasil menambahkan barang')

def view_items():
    st.write(st.session_state['df'])
    total_items = st.session_state['df']['Jumlah'].sum()
    st.write(f"Total barang: {total_items}")

def delete_item(name, quantity):
    item_index = st.session_state['df'][st.session_state['df']['Nama Barang'] == name].index[0]
    if st.session_state['df'].loc[item_index, 'Jumlah'] < quantity:
        st.warning('Jumlah yang akan dihapus lebih besar dari jumlah yang ada')
        return
    if st.session_state['df'].loc[item_index, 'Jumlah'] > quantity:
        st.session_state['df'].loc[item_index, 'Jumlah'] -= quantity
    else:
        st.session_state['df'].loc[item_index, 'Tanggal Pengembalian'] = date.today()  # Perbarui tanggal pengembalian
        st.session_state['df'] = st.session_state['df'].drop(item_index)
    save_items(st.session_state['username'], st.session_state['df'])  # Simpan item setelah menghapus barang
    st.success('Berhasil menghapus barang')

def search_item(name=None, category=None):
    df = st.session_state['df']
    if name:
        df = df[df['Nama Barang'] == name]
    if category:
        df = df[df['Kategori'] == category]
    return df

def edit_item(old_name, new_name, quantity, category, weight, return_date):
    if not new_name or not category:
        st.warning('Nama barang dan kategori tidak boleh kosong')
        return
    if quantity <= 0 or weight <= 0:
        st.warning('Jumlah dan berat harus lebih besar dari 0')
        return
    if return_date < date.today():
        st.warning('Tanggal pengembalian tidak boleh lebih awal dari hari ini')
        return
    item_index = st.session_state['df'][st.session_state['df']['Nama Barang'] == old_name].index[0]
    st.session_state['df'].loc[item_index, 'Nama Barang'] = new_name
    st.session_state['df'].loc[item_index, 'Jumlah'] = quantity
    st.session_state['df'].loc[item_index, 'Kategori'] = category
    st.session_state['df'].loc[item_index, 'Berat (Kg)'] = weight
    st.session_state['df'].loc[item_index, 'Tanggal Pengembalian'] = return_date
    save_items(st.session_state['username'], st.session_state['df'])  # Simpan item setelah mengedit barang
    st.success('Berhasil mengedit barang')

def export_data():
    st.session_state['df'].to_csv('data.csv')
    st.download_button(label='Download data', data=open('data.csv', 'rb'), file_name='data.csv')

def generate_report():
    total_items = st.session_state['df']['Jumlah'].sum()
    total_weight = st.session_state['df']['Berat (Kg)'].sum()
    total_price = (total_weight // 5) * 20000 + (total_weight // 365) * 25000
    st.write(f"Total barang: {total_items}")
    st.write(f"Total berat: {total_weight} Kg")
    st.write(f"Total harga: Rp{total_price}")
