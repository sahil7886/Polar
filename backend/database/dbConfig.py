# ✅ MongoDB Connection Setup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo
import gridfs

# Use the provided connection URI
uri = "mongodb+srv://aaryasontakke0507:lV1yR2c5ichbdZ7h@cluster0.axpym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["polar_db"]
fs = gridfs.GridFS(db)


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
