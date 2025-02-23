from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from src.data.constants import MONGO_DB_URI

# Create a new client and connect to the server
client = MongoClient(MONGO_DB_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

DB = client['IoT']
TEMPERATURE_COLLECTION = DB['TEMPERATURE']
HUMIDITY_COLLECTION = DB['HUMIDITY']
MOTION_COLLECTION = DB['MOTION']

