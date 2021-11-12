from bson import ObjectId
from pymongo import MongoClient

mongo_client = MongoClient('localhost')
db = mongo_client['chatapp']

account_collection = db['accounts']


def create_account(email: str, username: str, password_hash: bytes, salt: bytes):
    user = account_collection.insert_one({
        'email': email,
        'username': username,
        'password_hash': password_hash,
        'salt': salt
    })
    print(f'email: {email} username: {username} hash: {password_hash} salt: {salt}')
    return user


def get_account(username: str):
    return account_collection.find_one({'username': username})
