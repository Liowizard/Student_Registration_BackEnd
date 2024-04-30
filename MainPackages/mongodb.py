import json
import os
import time

from bson import json_util
from dotenv import load_dotenv
from pymongo import MongoClient

from MainPackages.email_otp import sendEmail
from MainPackages.FileStorage import getImageAndConverBoBase64

load_dotenv()


connectionString = os.getenv("connectionString")


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

    result = {
        "password": result["password"],
        "Approval_Status": result["Approval_Status"],
    }

    if result:
        return result


def DataForApproval():
    begin = time.time()
    client = MongoClient(connectionString)

    db = client.get_database()

    collection = db["users"]

    query = {"Approval_Status": "Yet to approve"}

    result = collection.find(query)

    user_list = []
    for user in result:

        capturedImages = []
        for image in user["biometric_data"]["face"]:
            capturedImages.append(
                f"data:image/jpeg;base64,{getImageAndConverBoBase64(image)}"
            )
        file = "data:image/jpeg;base64," + getImageAndConverBoBase64(
            user["biometric_data"]["Document"]
        )
        user["captured_images"] = capturedImages
        user["file"] = file

        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        user_list.append(user)

    client.close()

    if user_list:
        end = time.time()
        print(f"Total time to get the data from MongoDB {end - begin}")
        # print(user_list)
        return user_list


def update_approval_status(data):
    email = data["email"]
    status = data["Approval_Status"]

    if status == "Approved":
        # Update Approval_Status to 'Approved'
        query = {"email": email}
        update = {"$set": {"Approval_Status": "Approved"}}
        collection.update_one(query, update)
        print(f"Approval status for {email} updated to 'Approved'")
    elif status == "Rejected":
        Reason = data["Reason"]
        # Delete the document with the given email
        sendEmail(email, Reason)
        query = {"email": email}
        result = collection.delete_one(query)
        if result.deleted_count == 1:
            print(f"Entry with email {email} deleted")
        else:
            print(f"No entry found with email {email}")
    else:
        print("Invalid Approval_Status")
