import json
import os

from flask import Flask, request, session
from flask_cors import CORS

from MainPackages.email_otp import sendEmailVerificationRequest
from MainPackages.FileStorage import getImageAndConverBoBase64, uploadImageFromBase64
from MainPackages.mongodb import getDataFromDB, getPassword, sendDataToDB

app = Flask(__name__)

cors = CORS(app)


app.secret_key = "EmailAuthentication"


@app.route("/verify", methods=["POST"])
def verify():
    rec_email = request.get_json()
    rec_email = rec_email.get("email")

    print("rec_email)", rec_email)

    current_otp = sendEmailVerificationRequest(
        receiver=rec_email
    )  # this function sends otp to the receiver and also returns the same otp for our session storage
    print("current_otp", current_otp)
    session["current_otp"] = current_otp
    return {"current_otp": str(current_otp)}


@app.route("/sendUserPasword", methods=["POST", "get"])
def sendUserPasword():
    Email = request.args.get("userEmail")
    Password = getPassword(Email)
    if Password:
        print("Passwords", Password)
        return {"password": Password}
    else:
        return {"message": "Invalid User"}


@app.route("/sendData", methods=["POST", "get"])
def sendData():
    Email = request.args.get("userEmail")
    print("json_data", Email)
    data = getDataFromDB(Email)
    print("data", data)
    if data:
        capturedImages = []
        for image in data["biometric_data"]["face"]:
            capturedImages.append(
                f"data:image/jpeg;base64,{getImageAndConverBoBase64(image)}"
            )
        file = "data:image/jpeg;base64," + getImageAndConverBoBase64(
            data["biometric_data"]["Document"]
        )
        data["captured_images"] = capturedImages
        data["file"] = file
        return data
    else:
        return {"Note": "NewUser"}


@app.route("/GetData", methods=["POST"])
def GetData():
    json_data = request.form["json_data"]
    json_data = json.loads(json_data)
    image_number = 1
    email = json_data["email"]
    image_url = []
    for images in json_data["capturedImages"]:

        images = images.split(";base64,")[1]  # len("data:image/jpeg;base64,")

        # images = images[prefix_length:]

        imagePath = f"student_face/{email}/image{image_number}.png"
        image_url.append(imagePath)

        uploadImageFromBase64(imagePath, images)
        image_number += image_number

    print("image_url", image_url)

    file = json_data["file"]
    file = file.split(";base64,")[1]
    file_name = "student_ID/" + json_data["email"] + ".png"

    uploadImageFromBase64(file_name, file)
    biometric_data = {"face": image_url, "Document": file_name}

    json_data["biometric_data"] = biometric_data

    sendDataToDB(json_data)

    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
