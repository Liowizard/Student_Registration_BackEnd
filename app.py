import json

from flask import Flask, request, session
from flask_cors import CORS

from email_otp import sendEmailVerificationRequest
from mongodb import get_data_from_db, send_data_to_db
from s3_bucket import get_image_and_conver_to_base64, upload_image_from_base64

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
    return current_otp


@app.route("/send_Data", methods=["POST", "get"])
def send_Data():
    Email = request.args.get("userEmail")
    print("json_data", Email)
    data = get_data_from_db(Email)
    print("data", data)
    capturedImages = []
    for image in data["biometric_data"]["face"]:
        capturedImages.append(
            f"data:image/jpeg;base64,{get_image_and_conver_to_base64(image)}"
        )
    file = "data:image/jpeg;base64," + get_image_and_conver_to_base64(
        data["biometric_data"]["Document"]
    )
    data["captured_images"] = capturedImages
    data["file"] = file
    return data


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

        image_path = f"student_face/{email}/image{image_number}.png"
        image_url.append(image_path)

        upload_image_from_base64(image_path, images)
        image_number += image_number

    print("image_url", image_url)

    file = json_data["file"]
    file = file.split(";base64,")[1]
    file_name = "uploads/" + json_data["email"] + ".png"

    upload_image_from_base64(file_name, file)
    biometric_data = {"face": image_url, "Document": file_name}

    json_data["biometric_data"] = biometric_data

    send_data_to_db(json_data)

    return "done"


if __name__ == "__main__":
    app.run(debug=True)
