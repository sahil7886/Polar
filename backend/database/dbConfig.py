# ✅ MongoDB Connection Setup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
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
    users_collection = db["users"]
    videos_collection = db["videos"]

    user = users_collection.find_one({"_id": ObjectId("67ba811352fcae1c36e18adc")})
    print(user)

    # video = videos_collection.find_one({}, sort=[("_id", -1)])
    # print(video)

except Exception as e:
    print(f"❌ Connection failed: {e}")
