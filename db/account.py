from pymongo import MongoClient

from db import HOST

mongo_client = MongoClient(HOST)
db = mongo_client['chatapp']

account_collection = db['accounts']


def create_account(email: str, username: str, password_hash: str, salt: str):
    if not get_account(username):
        user = account_collection.insert_one({
            'email': email,
            'username': username,
            'password_hash': password_hash,
            'salt': salt
        })
        print(f'email: {email} username: {username} hash: {password_hash} salt: {salt}')
        return user
    else:
        return None


def get_account(username: str):
    return account_collection.find_one({'username': username})

def get_account_from_token(auth_token_hash: str):
    return account_collection.find_one({'auth_token_hash': auth_token_hash})

def get_account_from_password(password_hash: str):
    return account_collection.find_one({'password_hash': password_hash})

def add_token(username: str, auth_token_hash: str):
    account_collection.update_one(
        {'username': username},
        {'$set': {'auth_token_hash': auth_token_hash}})
