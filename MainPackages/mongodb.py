import json
import os
import time

from bson import json_util
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


connectionString = os.getenv(
    "connectionString"
)  # + "digischeduler?retryWrites=true&w=majority"
print("connection_string" + connectionString)

client = MongoClient(connectionString)


db = client.get_database()

collection = db["users"]


def getDataFromDB(email):
    begin = time.time()
    client = MongoClient(connectionString)

    db = client.get_database()

    collection = db["users"]

    query = {"email": email}

    result = collection.find_one(query)
    result = json.loads(json_util.dumps(result))

    client.close()

    if result:
        end = time.time()
        print(f"Total time to get the data from MongoDB {end - begin}")
        return result
        # print(result)


def sendDataToDB(data):
    data.pop("capturedImages")
    data.pop("file")
    print(data)

    db = client.get_database()
    collection = db["users"]
    # Specify the filter based on the email field
    filter_query = {"email": data["email"]}

    # Update the document if it exists, otherwise insert a new one
    update_result = collection.update_one(filter_query, {"$set": data}, upsert=True)

    if update_result.upserted_id:
        return "Document inserted"
    else:
        return "Document updated"


def getPassword(email):
    db = client.get_database()
    collection = db["users"]

    query = {"email": email}

    result = collection.find_one(query)

    if result:
        return result["password"]
