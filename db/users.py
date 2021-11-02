from bson import ObjectId
from pymongo import MongoClient

mongo_client = MongoClient('mongo')
db = mongo_client['chatapp']

user_collection = db['users']


def create_user(email: str, username: str):
    user = user_collection.insert_one({'email': email, 'username': username})
    print(f'{email}: {username}')
    return user


def get_single_user(user_id: str):
    return user_collection.find_one({'_id': ObjectId(user_id)})


def get_users():
    return user_collection.find()


def update_user(user_id: str, email: str, username: str):
    return user_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {
            'email': email,
            'username': username
        }})


def delete_user(user_id: str):
    return user_collection.delete_one({'_id': ObjectId(user_id)})
