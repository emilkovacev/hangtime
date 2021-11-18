from bson import ObjectId

from models import db
from datetime import datetime

event_collection = db['events']

def create_event(event_name: str, description: str, start_time: datetime, end_time: datetime):
    event = event_collection.insert_one({
        'event_name': event_name,
        'description': description,
        'start_time': start_time,
        'end_time': end_time,
    })

    print(f'Registered: {event_name}'
          f'description: {description}'
          f'start_time: {start_time}'
          f'end_time: {end_time}')

    return event

def find_event(_id: ObjectId):
    return event_collection.find_one({'_id': _id})

