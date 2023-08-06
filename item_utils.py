import hashlib
import json
import pandas as pd
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    return users

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

def login(user, password):
    users = load_users()
    if user in users:
        user_data = users[user]
        # Jika password disimpan sebagai dictionary, ambil password dari dictionary
        if isinstance(user_data, dict) and 'password' in user_data:
            stored_password = user_data['password']
        # Jika password disimpan sebagai string, gunakan string tersebut
        elif isinstance(user_data, str):
            stored_password = user_data
        else:
            return False
        return stored_password == hash_password(password)
    return False

def register(user, password):
    users = load_users()
    if user in users:
        return False
    users[user] = hash_password(password)
    save_users(users)
    # Buat file profil untuk pengguna baru
    profile = pd.DataFrame([['', '', '', '']], columns=['Nama', 'Email', 'Alamat', 'No HP'])
    save_profile(user, profile)
    return True

def save_profile(username, df):
    df.to_csv(f'{username}_profile.csv', index=False)

def update_profile(username, name, email, address, phone):
    df = load_profile(username)
    if df.empty:
        # Jika DataFrame kosong, tambahkan baris baru
        df.loc[0] = [name, email, address, phone]
    else:
        df.loc[0, 'Nama'] = name
        df.loc[0, 'Email'] = email
        df.loc[0, 'Alamat'] = address
        df.loc[0, 'No HP'] = phone
    save_profile(username, df)
    return True

def load_profile(username):
    if os.path.exists(f'{username}_profile.csv'):
        return pd.read_csv(f'{username}_profile.csv')
    else:
        # Jika file profil pengguna tidak ada, kembalikan DataFrame dengan satu baris kosong
        return pd.DataFrame([['', '', '', '']], columns=['Nama', 'Email', 'Alamat', 'No HP'])
