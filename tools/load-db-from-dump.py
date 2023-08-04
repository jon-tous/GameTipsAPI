import json
from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient


def json_object_hook(d):
    """Custom JSON decoder object hook to handle ObjectId deserialization"""

    for key, value in d.items():
        # Find string that resembles a BSON ObjectId
        if isinstance(value, str) and len(value) == 24 and all(c in '0123456789abcdef' for c in value):
            # Convert string to ObjectID
            d[key] = ObjectId(value)
    return d


# Read the JSON file
with open("mongo_data.json", "r") as f:
    data_to_import = json.load(f, object_hook=json_object_hook)

# Connect to the MongoDB database
config = dotenv_values("../.env")
uri = f"mongodb+srv://{config['USER']}:{config['PASSWORD']}@{config['CLUSTER']}/?retryWrites=true&w=majority"
mongodb_client = MongoClient(uri)
db = mongodb_client[config["DB_NAME"]]

# Send a ping to confirm a successful connection
try:
    mongodb_client.admin.command("ping")
    print(f"Connected to the MongoDB database: {db.name}")
except Exception as e:
    print(e)

# Wipe the database in case anything exists in it
for collection_name in db.list_collection_names():
    db[collection_name].delete_many({})

# Create collections and insert documents
for collection_name, documents in data_to_import.items():
    collection = db[collection_name]
    collection.insert_many(documents)

print(f"Data imported successfully into the MongoDB database {db.name}")
