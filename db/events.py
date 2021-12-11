from bson import ObjectId
from pymongo import MongoClient
from db import conn_str


mongo_client = MongoClient(conn_str, serverSelectionTimeoutMS=5000)
db = mongo_client['chatapp']

event_collection = db['events']

def create_event(event_name: str, description: str, start_time: str, end_time: str, color: str):
    event = event_collection.insert_one({
        'event_name': event_name,
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
        'color': color
    })

    print(f'Registered: {event_name}\n'
          f'description: {description}\n'
          f'start_time: {start_time}\n'
          f'end_time: {end_time}\n'
          f'color: {color}\n')

    return event

def dict_event(event_name: str, description: str, start_time: str, end_time: str, color: str):
    event = {
        'event_name': event_name,
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
        'color': color
    }
    return event

def find_event(_id: ObjectId):
    return event_collection.find_one({'_id': _id})

def all_events():
    return event_collection.find()
