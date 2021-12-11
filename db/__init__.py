import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = "chatapp"

conn_str = f"mongodb+srv://{USERNAME}:{PASSWORD}@hangtime.aryp3.mongodb.net/{DATABASE}?retryWrites=true&w=majority"
