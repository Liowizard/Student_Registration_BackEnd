import json

from bson import json_util
from pymongo import MongoClient

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


def send_data_to_db(data):

    data.pop("capturedImages")

    print(data)

    db = client.get_database()

    collection = db["users"]

    collection.insert_one(data)

    return "done"
