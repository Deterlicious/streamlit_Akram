import pandas as pd
import streamlit as st

def load_items(user):
    try:
        with open(f'{user}_items.json', 'r') as f:
            items = pd.read_json(f)
    except FileNotFoundError:
        items = pd.DataFrame(columns=['Nama Barang', 'Jumlah', 'Kategori', 'Berat (Kg)'])
    return items

def save_items(user, items):
    with open(f'{user}_items.json', 'w') as f:
        items.to_json(f)

def add_item(name, quantity, category, weight):
    new_row = pd.DataFrame({'Nama Barang': [name], 'Jumlah': [quantity], 'Kategori': [category], 'Berat (Kg)': [weight]})
    st.session_state['df'] = pd.concat([st.session_state['df'], new_row], ignore_index=True)
    st.session_state['df'].index = st.session_state['df'].index + 1  # Mengubah indeks dari 0 menjadi 1

def view_items():
    st.write(st.session_state['df'])
    total_items = st.session_state['df']['Jumlah'].sum()
    st.write(f"Total barang: {total_items}")

def delete_item(name, quantity):
    item_index = st.session_state['df'][st.session_state['df']['Nama Barang'] == name].index[0]
    if st.session_state['df'].loc[item_index, 'Jumlah'] > quantity:
        st.session_state['df'].loc[item_index, 'Jumlah'] -= quantity
    else:
        st.session_state['df'] = st.session_state['df'].drop(item_index)
    save_items(st.session_state['username'], st.session_state['df'])  # Simpan item setelah menghapus barang

def search_item(name):
    return st.session_state['df'][st.session_state['df']['Nama Barang'] == name]

def edit_item(old_name, new_name, quantity, category, weight):
    item_index = st.session_state['df'][st.session_state['df']['Nama Barang'] == old_name].index[0]
    st.session_state['df'].loc[item_index, 'Nama Barang'] = new_name
    st.session_state['df'].loc[item_index, 'Jumlah'] = quantity
    st.session_state['df'].loc[item_index, 'Kategori'] = category
    st.session_state['df'].loc[item_index, 'Berat (Kg)'] = weight
    save_items(st.session_state['username'], st.session_state['df'])  # Simpan item setelah mengedit barang

def export_data():
    st.session_state['df'].to_csv('data.csv')
    st.download_button(label='Download data', data=open('data.csv', 'rb'), file_name='data.csv')

