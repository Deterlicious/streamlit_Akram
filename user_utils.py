import hashlib
import json

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
    if user in users and users[user] == hash_password(password):
        return True
    return False

def register(user, password):
    users = load_users()
    if user in users:
        return False
    users[user] = hash_password(password)
    save_users(users)
    return True

def update_profile(user, name, email, address, phone, loan_duration):
    users = load_users()
    if user in users:
        users[user] = {'password': users[user], 'name': name, 'email': email, 'address': address, 'phone': phone, 'loan_duration': loan_duration.strftime('%Y-%m-%d')}
        save_users(users)
        return True
    return False

def load_profile(user):
    users = load_users()
    if user in users:
        profile = users[user]
        profile['loan_duration'] = pd.to_datetime(profile['loan_duration'])
        return profile
    return None
