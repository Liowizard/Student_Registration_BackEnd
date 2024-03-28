import json
import os

from bson import json_util
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


connection_string = os.getenv(
    "connection_string"
)  # + "digischeduler?retryWrites=true&w=majority"

data_structures = {
    "firstName": "",
    "middleName": "",
    "lastName": "",
    "dob": "",
    "gender": "",
    "mobileNumber": "",
    "capturedImages": None,
    "userEmail": "",
    "userpassword": None,
}


client = MongoClient(connection_string)


db = client.get_database()

collection = db["users"]


def get_data_from_db(email):
    client = MongoClient(connection_string)

    db = client.get_database()

    collection = db["users"]

    query = {"email": email}

    result = collection.find_one(query)
    result = json.loads(json_util.dumps(result))

    client.close()

    if result:
        return result
        # print(result)
    else:
        return {"error": "Could not find user with this email"}


# def send_data_to_db(data):

#     data.pop("capturedImages")

#     print(data)

#     db = client.get_database()

#     collection = db["users"]

#     collection.insert_one(data)

#     return "done"


def send_data_to_db(data):
    data.pop("capturedImages")
    print(data)

    db = client.get_database()
    collection = db["users"]
    print(data["email"])
    # Specify the filter based on the email field
    filter_query = {"email": data["email"]}

    # Update the document if it exists, otherwise insert a new one
    update_result = collection.update_one(filter_query, {"$set": data}, upsert=True)

    if update_result.upserted_id:
        return "Document inserted"
    else:
        return "Document updated"
