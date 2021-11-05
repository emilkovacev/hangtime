from pymongo import MongoClient

mongo_client = MongoClient('mongo')
db = mongo_client['hangtime']

message_collection = db['events']

def create_event()
