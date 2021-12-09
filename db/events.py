from bson import ObjectId

from pymongo import MongoClient

from db import HOST
mongo_client = MongoClient(HOST)
db = mongo_client['chatapp']

event_collection = db['events']

def create_event(event_name: str, description: str, start_time: str, end_time: str):
    event = event_collection.insert_one({
        'event_name': event_name,
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
    })

    print(f'Registered: {event_name}\n'
          f'description: {description}\n'
          f'start_time: {start_time}\n'
          f'end_time: {end_time}\n')

    return event

def find_event(_id: ObjectId):
    return event_collection.find_one({'_id': _id})

def all_events():
    return event_collection.find()
