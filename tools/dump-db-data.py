import json
from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle ObjectId serialization"""

    def default(self, o):  # override from superclass
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# Create a new client and connect to the server
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

# Fetch all collections and documents
data_to_export = {}
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    documents = list(collection.find())
    data_to_export[collection_name] = documents

# Store the dumped data in a local JSON file
with open("mongo_data.json", "w") as f:
    json.dump(data_to_export, f, indent=4, cls=JSONEncoder)

print("Data exported successfully to 'mongo_data.json'")
