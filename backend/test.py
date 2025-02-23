from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# Use the provided connection URI
uri = "mongodb+srv://aaryasontakke0507:lV1yR2c5ichbdZ7h@cluster0.axpym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=false"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client["polar_db"]
users_collection = db["users"]

user = users_collection.find_one({"_id": ObjectId("67ba811352fcae1c36e18adc")})
print(user)
