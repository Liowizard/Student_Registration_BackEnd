import json

from flask import Flask, jsonify, request, session
from flask_cors import CORS

from email_otp import sendEmailVerificationRequest
from mongodb import get_data_from_db, send_data_to_db
from s3_bucket import upload_image_from_base64

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
    # data = jsonify(data)
    return data


@app.route("/GetData", methods=["POST"])
def GetData():
    json_data = request.form["json_data"]
    json_data = json.loads(json_data)

    for images in json_data["capturedImages"]:
        print("json_data", json_data["email"])
    # upload_image_from_base64("student_face", base64_image, image_name)

    send_data_to_db(json_data)
    file = request.files["file"]
    file.save("uploads/" + file.filename)
    return "done"


if __name__ == "__main__":
    app.run(debug=True)
