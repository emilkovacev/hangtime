from models import db

user_collection = db['events']

def create_user(email: str, username: str, password_hash: str, salt: str):
    user = user_collection.insert_one({
        'email': email,
        'username': username,
        'password_hash': password_hash,
        'salt': salt,
        'events': []
    })

    print(f'Registered: {username}'
          f'email: {email}'
          f'hash: {password_hash}'
          f'salt: {salt}')

    return user

def find_user(username: str):
    return user_collection.find_one({'username': username})

