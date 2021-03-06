from pymongo import MongoClient

from db import HOST

mongo_client = MongoClient(HOST)
db = mongo_client['chatapp']

message_collection = db['messages']

def create_message(username: str, comment: str):
    message_collection.insert_one({'username': username, 'comment': comment})
    print(f'{username}: {comment}')

def get_messages():
    return message_collection.find()
