from pymongo import MongoClient

mongo_client = MongoClient('localhost')
db = mongo_client['message_share']

message_collection = db['messages']

def create_message(user: str, message: str):
    message_collection.insert_one({'username': user, 'comment': message})
    print(f'{user}: {message}')

def get_messages():
    return message_collection.find()
